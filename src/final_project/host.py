class Host:
    def __init__(self, host_id, place, city):
        """
        host_id : int
            Unique ID of the host.
        place : Place
            The initial place owned by this host.
        city : City
            Reference to the city.
        """
        self.host_id = host_id
        self.city = city

        self.area = place.area                  # area = initial place's area
        self.profits = 0                        # starting funds
        self.assets = {place.place_id}          # IDs of all owned properties

    # ----------------------------------------------------------
    # Update host profits based on earnings from all owned places
    # ----------------------------------------------------------
    def update_profits(self):
        """
        For each owned place:
            profits += rate * occupancy
        """
        for pid in self.assets:
            place = self.city.places[pid]
            self.profits += place.rate * place.occupancy

    # ----------------------------------------------------------
    # Host attempts to buy any neighbouring properties
    # ----------------------------------------------------------
    def make_bids(self):
        """
        Returns a list of bids. Each bid is a dictionary:
        {
            'place_id': pid,
            'seller_id': place.host_id,
            'buyer_id': self.host_id,
            'spread': self.profits - ask_price,
            'bid_price': self.profits
        }
        """
        bids = []
        candidate_ids = set()

        # Identify all neighbours of all owned assets
        for pid in self.assets:
            neighbours = self.city.places[pid].neighbours
            for n in neighbours:
                if n not in self.assets:
                    candidate_ids.add(n)

        # For each opportunity, try to bid
        for pid in candidate_ids:
            place = self.city.places[pid]

            # Get latest price
            current_step = max(place.price.keys())
            ask_price = place.price[current_step]

            if self.profits >= ask_price:
                bids.append({
                    'place_id': pid,
                    'seller_id': place.host_id,
                    'buyer_id': self.host_id,
                    'spread': self.profits - ask_price,
                    'bid_price': self.profits
                })

        return bids
