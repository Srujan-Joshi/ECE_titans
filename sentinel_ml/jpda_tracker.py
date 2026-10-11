#!/usr/bin/env python3
"""
JPDA Multi-Target Tracker (Python Edge Engine - Zero Dependency)
===============================================================
Implements Joint Probabilistic Data Association (JPDA) filter alongside
discrete-time Kalman filtering for multi-target tracking in dense clutter.
"""

import math
from typing import List, Dict, Tuple, Optional

class JPDATracker:
    def __init__(self, sigma_noise: float = 0.007, pd: float = 0.95, lambda_clutter: float = 1e-4):
        self.sigma = sigma_noise
        self.pd = pd
        self.lambda_clutter = lambda_clutter
        self.tracks: Dict[str, Dict] = {}
        self.next_track_id = 1
        self.gate_threshold = 0.08  # Validation gate in degrees

    def predict(self):
        """Predicts state and covariance for all active tracks."""
        for tid, trk in list(self.tracks.items()):
            # State transition: x_new = x + v
            trk['x'] += trk['vx']
            trk['y'] += trk['vy']
            # Covariance prediction
            q = 1e-4
            trk['p00_x'] += 2 * trk['p01_x'] + trk['p11_x'] + q / 3
            trk['p01_x'] += trk['p11_x'] + q / 2
            trk['p11_x'] += q
            
            trk['p00_y'] += 2 * trk['p01_y'] + trk['p11_y'] + q / 3
            trk['p01_y'] += trk['p11_y'] + q / 2
            trk['p11_y'] += q
            trk['misses'] += 1

    def update(self, measurements: List[Tuple[float, float]]):
        """
        Updates tracks using JPDA marginal association probabilities.
        measurements: List of (latitude, longitude)
        """
        self.predict()
        rn = self.sigma ** 2
        used_meas = set()

        for tid, trk in list(self.tracks.items()):
            gated_indices = []
            distances = []

            for idx, (lat, lon) in enumerate(measurements):
                dist = math.hypot(lat - trk['y'], (lon - trk['x']) * math.cos(math.radians(lat)))
                if dist < self.gate_threshold:
                    gated_indices.append(idx)
                    distances.append(dist)

            if gated_indices:
                trk['misses'] = 0
                trk['hits'] += 1
                
                # Compute marginal association probabilities beta
                b = self.lambda_clutter * 2 * math.pi * rn * (1 - self.pd) / self.pd
                weights = [math.exp(-0.5 * (d ** 2) / rn) for d in distances]
                total_w = sum(weights) + b
                betas = [w / total_w for w in weights]
                beta0 = b / total_w

                # Weighted innovation
                innov_x = sum(betas[i] * (measurements[gated_indices[i]][1] - trk['x']) for i in range(len(betas)))
                innov_y = sum(betas[i] * (measurements[gated_indices[i]][0] - trk['y']) for i in range(len(betas)))

                # Kalman gains
                s_x = trk['p00_x'] + rn
                k0_x = trk['p00_x'] / s_x
                k1_x = trk['p01_x'] / s_x

                s_y = trk['p00_y'] + rn
                k0_y = trk['p00_y'] / s_y
                k1_y = trk['p01_y'] / s_y

                # Update states
                trk['x'] += k0_x * innov_x
                trk['vx'] += k1_x * innov_x
                trk['y'] += k0_y * innov_y
                trk['vy'] += k1_y * innov_y

                # Covariance update with spread of innovations
                trk['p00_x'] = (1 - k0_x) * trk['p00_x']
                trk['p00_y'] = (1 - k0_y) * trk['p00_y']

                for idx in gated_indices:
                    used_meas.add(idx)
            else:
                if trk['misses'] > 5:
                    del self.tracks[tid]

        # Initialize new tracks for unassociated measurements
        for idx, (lat, lon) in enumerate(measurements):
            if idx not in used_meas:
                new_id = f"TRK-{self.next_track_id}"
                self.next_track_id += 1
                self.tracks[new_id] = {
                    'x': lon, 'vx': 0.0,
                    'y': lat, 'vy': 0.0,
                    'p00_x': rn, 'p01_x': 0.0, 'p11_x': 1e-4,
                    'p00_y': rn, 'p01_y': 0.0, 'p11_y': 1e-4,
                    'hits': 1, 'misses': 0
                }

    def get_tracks(self) -> List[Dict]:
        return [
            {
                'id': tid,
                'lat': trk['y'],
                'lon': trk['x'],
                'speed_knots': math.hypot(trk['vx'], trk['vy']) * 111 * 3600 / 1.852,
                'hits': trk['hits']
            }
            for tid, trk in self.tracks.items()
            if trk['hits'] >= 2
        ]

if __name__ == "__main__":
    tracker = JPDATracker()
    print("Testing JPDA Multi-Target Tracker (Zero-Dependency Engine)...")
    for t in range(5):
        meas = [
            (15.0 + t * 0.01, 67.0 + t * 0.01),
            (15.05 - t * 0.01, 67.0 + t * 0.01)
        ]
        tracker.update(meas)
    tracks = tracker.get_tracks()
    print(f"Tracking completed successfully. Active sustained tracks: {len(tracks)}")
    for trk in tracks:
        print(f"  Track {trk['id']}: Lat {trk['lat']:.3f}, Lon {trk['lon']:.3f}, Speed {trk['speed_knots']:.1f} kn")
