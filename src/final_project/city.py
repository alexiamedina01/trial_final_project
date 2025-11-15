import pandas as pd
from .place import Place
from .host import Host

class City:
    def __init__(self, size, area_rates):
        """
        size : int
            Grid is size × size (e.g., 10 × 10)
        area_rates : dict
            Nightly rate ranges for each of the 4 areas.
        """
        self.grid_size = size
        self.area_rates = area_rates
        self.step = 0

        self.places = []
        self.hosts = []

    # ----------------------------------------------------------
    # Initialize Places and Hosts
    # ----------------------------------------------------------
    def initialize(self):
        # Create places
        for grid in range(self.grid_size * self.grid_size):
            place = Place(place_id=grid, host_id=grid, city=self)
            self.places.append(place)

        # Setup each place
        for place in self.places:
            place.setup()

        # Create hosts (one per place initially)
        for place in self.places:
            host = Host(host_id=place.host_id, place=place, city=self)
            self.hosts.append(host)

    # ----------------------------------------------------------
    # Approve bids based on spread (sorted descending)
    # ----------------------------------------------------------
    def approve_bids(self, bids):
        if not bids:
            return []

        df = pd.DataFrame(bids)
        df = df.sort_values(by="spread", ascending=False)

        approved = []
        bought_places = set()
        buyers_used = set()

        for _, bid in df.iterrows():
            pid = bid['place_id']
            buyer = bid['buyer_id']

            if pid not in bought_places and buyer not in buyers_used:
                approved.append(bid.to_dict())
                bought_places.add(pid)
                buyers_used.add(buyer)

        return approved

    # ----------------------------------------------------------
    # Execute approved transactions
    # ----------------------------------------------------------
    def execute_transactions(self, transactions):
        for tr in transactions:
            pid = tr['place_id']
            buyer_id = tr['buyer_id']
            seller_id = tr['seller_id']
            price = tr['bid_price']

            place = self.places[pid]
            buyer = self.hosts[buyer_id]
            seller = self.hosts[seller_id]

            # Transfer property
            seller.assets.remove(pid)
            buyer.assets.add(pid)

            # Transfer funds
            buyer.profits -= price
            seller.profits += price

            # Update owner
            place.host_id = buyer_id

            # Record new sale price
            place.price[self.step] = price

    # ----------------------------------------------------------
    # Market clearing
    # ----------------------------------------------------------
    def clear_market(self):
        all_bids = []

        # Collect all bids
        for host in self.hosts:
            bids = host.make_bids()
            all_bids.extend(bids)

        # Approve bids
        approved = self.approve_bids(all_bids)

        # Execute transactions
        if approved:
            self.execute_transactions(approved)

        return approved

    # ----------------------------------------------------------
    # Iterate one time step
    # ----------------------------------------------------------
    def iterate(self):
        self.step += 1

        # Update occupancy for all places
        for place in self.places:
            area = place.area
            area_places = [p.rate for p in self.places if p.area == area]
            area_mean = sum(area_places) / len(area_places)
            place.update_occupancy(area_mean)

        # Update profits
        for host in self.hosts:
            host.update_profits()

        # Clear market
        transactions = self.clear_market()
        return transactions

