# src/final_project/city.py
import pandas as pd
from .place import Place
from .host import Host

class City:
    def __init__(self, size, area_rates, bid_fraction=1.0):
        """
        size : int (grid size x size)
        area_rates : dict of ranges
        bid_fraction : fraction of profits hosts can use to bid
        """
        self.grid_size = size
        self.area_rates = area_rates
        self.step = 0

        self.places = []
        self.hosts = []

        self.bid_fraction = bid_fraction  # <-- ESTA ES LA CLAVE

    def initialize(self):
        total = self.grid_size * self.grid_size

        # Create places
        self.places = []
        for pid in range(total):
            place = Place(place_id=pid, host_id=pid, city=self)
            self.places.append(place)

        # Setup
        for place in self.places:
            place.setup()

        # Create hosts
        self.hosts = []
        for place in self.places:
            host = Host(host_id=place.host_id, place=place, city=self)
            self.hosts.append(host)

    def approve_bids(self, bids):
        if not bids:
            return []

        df = pd.DataFrame(bids)
        if df.empty:
            return []

        df = df.sort_values(by="spread", ascending=False)

        approved = []
        bought_places = set()
        buyers_used = set()

        for _, row in df.iterrows():
            pid = int(row["place_id"])
            buyer = int(row["buyer_id"])
            seller = int(row["seller_id"])

            if pid not in bought_places and buyer not in buyers_used:

                # ensure the seller still owns the property
                if self.places[pid].host_id == seller:
                    approved.append({
                        "place_id": pid,
                        "seller_id": seller,
                        "buyer_id": buyer,
                        "bid_price": float(row["bid_price"])
                    })
                    bought_places.add(pid)
                    buyers_used.add(buyer)

        return approved

    def execute_transactions(self, transactions):
        for tr in transactions:
            pid = tr["place_id"]
            buyer_id = tr["buyer_id"]
            seller_id = tr["seller_id"]
            price = tr["bid_price"]

            place = self.places[pid]
            buyer = self.hosts[buyer_id]
            seller = self.hosts[seller_id]

            # Transfer asset
            if pid in seller.assets:
                seller.assets.remove(pid)
            buyer.assets.add(pid)

            # Transfer money
            buyer.profits -= price
            seller.profits += price

            # Update ownership
            place.host_id = buyer_id

            # Update price history
            place.price[self.step] = price

    def clear_market(self):
        all_bids = []
        for host in self.hosts:
            bids = host.make_bids()
            all_bids.extend(bids)

        approved = self.approve_bids(all_bids)

        if approved:
            self.execute_transactions(approved)

        return approved

    def iterate(self):
        self.step += 1

        # Compute area means
        area_means = {}
        for area in range(4):
            rates = [p.rate for p in self.places if p.area == area]
            area_means[area] = sum(rates) / len(rates)

        # Update occupancy
        for place in self.places:
            place.update_occupancy(area_means[place.area])

        # Update profits
        for host in self.hosts:
            host.update_profits()

        # Market clearing
        transactions = self.clear_market()
        return transactions
