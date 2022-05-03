import numpy as np


class CoordTransformer:
    def __init__(self, config):
        self.config = config
        self.local_origin = None

    # https://qiita.com/sw1227/items/e7a590994ad7dcd0e8ab
    def latlng2xy(self, phi_deg, lambda_deg):
        phi_rad = np.deg2rad(phi_deg)
        lambda_rad = np.deg2rad(lambda_deg)
        phi0_rad = np.deg2rad(self.config.map_config.base_origin_latlng[0])
        lambda0_rad = np.deg2rad(self.config.map_config.base_origin_latlng[1])

        def A_array(n):
            A0 = 1 + (n**2) / 4.0 + (n**4) / 64.0
            A1 = -(3.0 / 2) * (n - (n**3) / 8.0 - (n**5) / 64.0)
            A2 = (15.0 / 16) * (n**2 - (n**4) / 4.0)
            A3 = -(35.0 / 48) * (n**3 - (5.0 / 16) * (n**5))
            A4 = (315.0 / 512) * (n**4)
            A5 = -(693.0 / 1280) * (n**5)
            return np.array([A0, A1, A2, A3, A4, A5])

        def alpha_array(n):
            a0 = np.nan
            a1 = (
                (1.0 / 2) * n
                - (2.0 / 3) * (n**2)
                + (5.0 / 16) * (n**3)
                + (41.0 / 180) * (n**4)
                - (127.0 / 288) * (n**5)
            )
            a2 = (13.0 / 48) * (n**2) - (3.0 / 5) * (n**3) + (557.0 / 1440) * (n**4) + (281.0 / 630) * (n**5)
            a3 = (61.0 / 240) * (n**3) - (103.0 / 140) * (n**4) + (15061.0 / 26880) * (n**5)
            a4 = (49561.0 / 161280) * (n**4) - (179.0 / 168) * (n**5)
            a5 = (34729.0 / 80640) * (n**5)
            return np.array([a0, a1, a2, a3, a4, a5])

        m0 = 0.9999
        a = 6378137.0
        F = 298.257222101

        n = 1.0 / (2 * F - 1)
        A_array = A_array(n)
        alpha_array = alpha_array(n)

        A_ = ((m0 * a) / (1.0 + n)) * A_array[0]
        S_ = ((m0 * a) / (1.0 + n)) * (A_array[0] * phi0_rad + np.dot(A_array[1:], np.sin(2 * phi0_rad * np.arange(1, 6))))

        lambda_c = np.cos(lambda_rad - lambda0_rad)
        lambda_s = np.sin(lambda_rad - lambda0_rad)

        t = np.sinh(
            np.arctanh(np.sin(phi_rad))
            - ((2 * np.sqrt(n)) / (1 + n)) * np.arctanh(((2 * np.sqrt(n)) / (1 + n)) * np.sin(phi_rad))
        )
        t_ = np.sqrt(1 + t * t)

        xi2 = np.arctan(t / lambda_c)
        eta2 = np.arctanh(lambda_s / t_)

        x = (
            A_
            * (
                xi2
                + np.sum(
                    np.multiply(
                        alpha_array[1:], np.multiply(np.sin(2 * xi2 * np.arange(1, 6)), np.cosh(2 * eta2 * np.arange(1, 6)))
                    )
                )
            )
            - S_
        )
        y = A_ * (
            eta2
            + np.sum(
                np.multiply(
                    alpha_array[1:], np.multiply(np.cos(2 * xi2 * np.arange(1, 6)), np.sinh(2 * eta2 * np.arange(1, 6)))
                )
            )
        )
        return x, y

    def xy2imagexy(self, x, y):
        if not self.local_origin:
            self.local_origin = self.latlng2xy(*self.config.map_config.map_bottom_left)

        return int((x - self.local_origin[0]) / self.config.map_config.resolution), int(
            (y - self.local_origin[1]) / self.config.map_config.resolution
        )

    def get_mapsize(self):
        return tuple(
            (
                (
                    np.array(self.latlng2xy(*self.config.map_config.map_top_right))
                    - np.array(self.latlng2xy(*self.config.map_config.map_bottom_left))
                )
                / self.config.map_config.resolution
            ).astype(int)
        )
