import random

class Place:
    def __init__(self, place_id, host_id, city):
        self.place_id = place_id
        self.host_id = host_id
        self.city = city

        # These get created in setup()
        self.neighbours = []
        self.area = None
        self.rate = None
        self.price = {}
        self.occupancy = None

    def setup(self):
        N = self.city.grid_size  # normally 10
        r = self.place_id // N   # row index
        c = self.place_id % N    # column index

        # --- 1. Adjacent neighbours (8-directional) ---
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]

        neighbours = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N:
                neighbours.append(nr * N + nc)

        self.neighbours = neighbours

        # --- 2. Determine area / quadrant ---
        half = N // 2  # 5 for a 10×10 grid

        if r < half and c < half:
            self.area = 0  # bottom-left
        elif r < half and c >= half:
            self.area = 1  # bottom-right
        elif r >= half and c < half:
            self.area = 2  # top-left
        else:
            self.area = 3  # top-right

        # --- 3. Assign nightly rate based on area interval ---
        low, high = self.city.area_rates[self.area]
        self.rate = random.uniform(low, high)

        # --- 4. Initialize price history ---
        self.price = {0: 900 * self.rate}

    def update_occupancy(self, area_mean):
        """
        area_mean : float
            Mean nightly rate of this listing's area.
        """
        if self.rate > area_mean:
            # More expensive → lower occupancy
            self.occupancy = random.randint(5, 15)
        else:
            # Cheaper or equal → higher occupancy
            self.occupancy = random.randint(10, 20)
