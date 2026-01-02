import csv
import json
import random
from datetime import timedelta
from faker import Faker
import requests
import gzip
import io

fake = Faker()
Faker.seed(42)

# Helper functions
def generate_customer():
    return {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "optionPreference": {"theme": random.choice(["dark", "light"])},
        "phone": fake.phone_number(),
        "methodPayment": {
            "type": random.choice(["credit_card", "paypal"]),
            "provider": fake.credit_card_provider()
        }
    }

def generate_manager():
    return {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "optionPreference": {"theme": random.choice(["dark", "light"])},
        "phone": fake.phone_number(),
        "iban": fake.iban()
    }

def generate_reservation():
    check_in = fake.date_between("-30d", "+30d")
    check_out = check_in + timedelta(days=random.randint(1,7))
    return {
        "checkInDate": check_in.isoformat(),
        "checkOutDate": check_out.isoformat(),
        "creationDate": fake.date_between("-60d", check_in).isoformat(),
        "adults": random.randint(1,4),
        "children": random.randint(0,2),
        "status": random.choice(["confirmed","cancelled","completed"])
    }

# POI data
famous_places_coords = {
    "Rome":[
        {"name":"Colosseo","coordinates":[41.8902,12.4922]},
        {"name":"Pantheon","coordinates":[41.8986,12.4768]},
        {"name":"Foro Romano","coordinates":[41.8925,12.4853]},
        {"name":"Piazza Navona","coordinates":[41.8992,12.4731]},
        {"name":"Vaticano","coordinates":[41.9029,12.4534]}
    ],
    "Paris":[
        {"name":"Torre Eiffel","coordinates":[48.8584,2.2945]},
        {"name":"Louvre","coordinates":[48.8606,2.3376]},
        {"name":"Notre-Dame","coordinates":[48.8530,2.3499]},
        {"name":"Montmartre","coordinates":[48.8867,2.3431]},
        {"name":"Museo d'Orsay","coordinates":[48.8600,2.3266]}
    ],
    "London":[
        {"name":"Big Ben","coordinates":[51.5007,-0.1246]},
        {"name":"Tower Bridge","coordinates":[51.5055,-0.0754]},
        {"name":"London Eye","coordinates":[51.5033,-0.1196]},
        {"name":"Buckingham Palace","coordinates":[51.5014,-0.1419]},
        {"name":"British Museum","coordinates":[51.5194,-0.1270]}
    ],
    "Berlin":[
        {"name":"Porta di Brandeburgo","coordinates":[52.5163,13.3777]},
        {"name":"Reichstag","coordinates":[52.5186,13.3762]},
        {"name":"Isola dei Musei","coordinates":[52.5169,13.4010]},
        {"name":"Checkpoint Charlie","coordinates":[52.5076,13.3904]},
        {"name":"Alexanderplatz","coordinates":[52.5219,13.4132]}
    ],
    "Madrid":[
        {"name":"Plaza Mayor","coordinates":[40.4154,-3.7074]},
        {"name":"Museo del Prado","coordinates":[40.4138,-3.6921]},
        {"name":"Palacio Real","coordinates":[40.4170,-3.7143]},
        {"name":"Parque del Retiro","coordinates":[40.4153,-3.6846]},
        {"name":"Puerta del Sol","coordinates":[40.4169,-3.7038]}
    ],
    "Lisbon":[
        {"name":"Torre di Belém","coordinates":[38.6916,-9.2156]},
        {"name":"Alfama","coordinates":[38.7129,-9.1305]},
        {"name":"Castelo de São Jorge","coordinates":[38.7139,-9.1334]},
        {"name":"Mosteiro dos Jerónimos","coordinates":[38.6971,-9.2065]},
        {"name":"Praça do Comércio","coordinates":[38.7071,-9.1366]}
    ],
    "Vienna":[
        {"name":"Schönbrunn Palace","coordinates":[48.1845,16.3122]},
        {"name":"St. Stephen's Cathedral","coordinates":[48.2082,16.3738]},
        {"name":"Belvedere Palace","coordinates":[48.1915,16.3805]},
        {"name":"Prater","coordinates":[48.2162,16.3989]},
        {"name":"Hofburg","coordinates":[48.2060,16.3658]}
    ],
    "Athens":[
        {"name":"Acropolis","coordinates":[37.9715,23.7257]},
        {"name":"Parthenon","coordinates":[37.9715,23.7266]},
        {"name":"Plaka","coordinates":[37.9755,23.7346]},
        {"name":"Temple of Olympian Zeus","coordinates":[37.9699,23.7333]},
        {"name":"National Archaeological Museum","coordinates":[37.9890,23.7330]}
    ],
    "Budapest":[
        {"name":"Buda Castle","coordinates":[47.4969,19.0396]},
        {"name":"Parliament","coordinates":[47.5070,19.0450]},
        {"name":"Chain Bridge","coordinates":[47.4980,19.0396]},
        {"name":"Fisherman's Bastion","coordinates":[47.5020,19.0344]},
        {"name":"Heroes' Square","coordinates":[47.5143,19.0773]}
    ],
    "Prague":[
        {"name":"Charles Bridge","coordinates":[50.0865,14.4114]},
        {"name":"Prague Castle","coordinates":[50.0903,14.3988]},
        {"name":"Old Town Square","coordinates":[50.0870,14.4208]},
        {"name":"Astronomical Clock","coordinates":[50.0871,14.4210]},
        {"name":"Wenceslas Square","coordinates":[50.0810,14.4265]}
    ],
    "Oslo":[
        {"name":"Opera House","coordinates":[59.9076,10.7532]},
        {"name":"Vigeland Park","coordinates":[59.9270,10.6983]},
        {"name":"Akershus Fortress","coordinates":[59.9078,10.7384]},
        {"name":"Nobel Peace Center","coordinates":[59.9120,10.7382]},
        {"name":"Karl Johans Gate","coordinates":[59.9122,10.7461]}
    ],
    "Copenhagen":[
        {"name":"Tivoli Gardens","coordinates":[55.6735,12.5681]},
        {"name":"Nyhavn","coordinates":[55.6803,12.5937]},
        {"name":"The Little Mermaid","coordinates":[55.6929,12.5994]},
        {"name":"Rosenborg Castle","coordinates":[55.6850,12.5833]},
        {"name":"Christiansborg Palace","coordinates":[55.6759,12.5831]}
    ],
    "Stockholm":[
        {"name":"Gamla Stan","coordinates":[59.3250,18.0700]},
        {"name":"Vasa Museum","coordinates":[59.3275,18.0916]},
        {"name":"Royal Palace","coordinates":[59.3276,18.0717]},
        {"name":"ABBA Museum","coordinates":[59.3277,18.0924]},
        {"name":"Skansen","coordinates":[59.3270,18.0970]}
    ]
}

def generate_poi_near_property(lat, lon, city, num_pois=5):
    city_places = famous_places_coords.get(city, [])
    return city_places[:num_pois]

# Download CSV from InsideAirbnb
def download_insideairbnb_csv(file_url):
    try:
        r = requests.get(file_url, timeout=20)
        r.raise_for_status()
        with gzip.open(io.BytesIO(r.content), mode='rt', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
        print(f"CSV scaricato ✅: {file_url}")
        return reader
    except Exception as e:
        print(f"Errore nel download CSV {file_url}: {e}")
        return []

# Generate Dataset for one city
def generate_dataset(listings_csv_url, reviews_csv_url, num_properties=50):
    listings = download_insideairbnb_csv(listings_csv_url)
    reviews_csv = download_insideairbnb_csv(reviews_csv_url)
    properties = []

    for row in listings[:num_properties]:
        amenities = row.get("amenities","").replace("{","").replace("}","").split(",")
        if amenities == [""]:
            amenities = [fake.word() for _ in range(5)]

        lat = float(row.get("latitude",0))
        lon = float(row.get("longitude",0))
        city_name = row.get("city","Unknown")

        property_data = {
            "name": row.get("name") or fake.company(),
            "address": row.get("neighbourhood_cleansed") or fake.address(),
            "description": row.get("description") or fake.text(max_nb_chars=500),
            "amenities": amenities,
            "photos": [row.get("picture_url")] if row.get("picture_url") else [fake.image_url() for _ in range(5)],
            "email": fake.company_email(),
            "country": row.get("country") or "Unknown",
            "region": row.get("state") or "Unknown",
            "city": city_name,
            "manager": generate_manager(),
            "rooms": [],
            "reservations": [],
            "reviews": [],
            "pointsOfInterest": generate_poi_near_property(lat, lon, city_name, num_pois=10),
            "coordinates": [lat, lon],
            "customers": []
        }

        # Rooms
        num_rooms = random.randint(3,5)
        for i in range(num_rooms):
            price_str = row.get("price","0").replace("$","").replace(",","").strip()
            try:
                price_adult = float(price_str) if price_str else random.uniform(30,200)
            except:
                price_adult = random.uniform(30,200)
            property_data["rooms"].append({
                "roomType": random.choice(["single","matrimonial","double","suite"]),
                "amenities": amenities,
                "name": f"Room {i+1}",
                "beds": random.randint(1,3),
                "photos": property_data["photos"],
                "status": "available",
                "capacityAdults": random.randint(1,4),
                "capacityChildren": random.randint(0,3),
                "pricePerNightAdults": round(price_adult,2),
                "pricePerNightChildren": round(random.uniform(10,50),2)
            })

        # Customers & reservations
        for _ in range(random.randint(10,20)):
            property_data["customers"].append(generate_customer())
            property_data["reservations"].append(generate_reservation())

        # Reviews
        property_reviews = 0
        for row_rev in reviews_csv:
            if property_reviews >= 50:
                break
            comment = row_rev.get("comments")
            text_review = comment if comment and comment.strip() != "" else fake.text(max_nb_chars=300)
            property_data["reviews"].append({
                "creationDate": row_rev.get("date","") or fake.date_between("-1y","today").isoformat(),
                "text": text_review,
                "rating": random.randint(3,5),
                "managerReply": fake.sentence() if random.choice([True,False]) else None
            })
            property_reviews += 1

        properties.append(property_data)

    return properties

# Generate Multi-city
def generate_dataset_multiple_cities(city_data, num_properties_per_city=50):
    all_properties = []
    for city, urls in city_data.items():
        print(f"Generando dati per {city}...")
        properties = generate_dataset(urls["listings"], urls["reviews"], num_properties=num_properties_per_city)
        all_properties.extend(properties)
    return all_properties

# Main
def main():
    city_data = {
        "Rome": {"listings":"https://data.insideairbnb.com/italy/lazio/rome/2025-09-14/data/listings.csv.gz",
                 "reviews":"https://data.insideairbnb.com/italy/lazio/rome/2025-09-14/data/reviews.csv.gz"},
        "Paris": {"listings":"https://data.insideairbnb.com/france/ile-de-france/paris/2025-09-12/data/listings.csv.gz",
                  "reviews":"https://data.insideairbnb.com/france/ile-de-france/paris/2025-09-12/data/reviews.csv.gz"},
        "London": {"listings":"https://data.insideairbnb.com/united-kingdom/england/london/2025-09-14/data/listings.csv.gz",
                   "reviews":"https://data.insideairbnb.com/united-kingdom/england/london/2025-09-14/data/reviews.csv.gz"},
        "Berlin": {"listings":"https://data.insideairbnb.com/germany/be/berlin/2025-09-23/data/listings.csv.gz",
                   "reviews":"https://data.insideairbnb.com/germany/be/berlin/2025-09-23/data/reviews.csv.gz"},
        "Madrid": {"listings":"https://data.insideairbnb.com/spain/comunidad-de-madrid/madrid/2025-09-14/data/listings.csv.gz",
                   "reviews":"https://data.insideairbnb.com/spain/comunidad-de-madrid/madrid/2025-09-14/data/reviews.csv.gz"},
        "Lisbon": {"listings":"https://data.insideairbnb.com/portugal/lisbon/lisbon/2025-09-21/data/listings.csv.gz",
                   "reviews":"https://data.insideairbnb.com/portugal/lisbon/lisbon/2025-09-21/data/reviews.csv.gz"},
        "Vienna": {"listings":"https://data.insideairbnb.com/austria/vienna/vienna/2025-09-14/data/listings.csv.gz",
                   "reviews":"https://data.insideairbnb.com/austria/vienna/vienna/2025-09-14/data/reviews.csv.gz"},
        "Athens": {"listings":"https://data.insideairbnb.com/greece/attica/athens/2025-09-26/data/listings.csv.gz",
                   "reviews":"https://data.insideairbnb.com/greece/attica/athens/2025-09-26/data/reviews.csv.gz"},
        "Budapest": {"listings":"https://data.insideairbnb.com/hungary/k%C3%B6z%C3%A9p-magyarorsz%C3%A1g/budapest/2025-09-25/data/listings.csv.gz",
                     "reviews":"https://data.insideairbnb.com/hungary/k%C3%B6z%C3%A9p-magyarorsz%C3%A1g/budapest/2025-09-25/data/reviews.csv.gz"},
        "Prague": {"listings":"https://data.insideairbnb.com/czech-republic/prague/prague/2025-09-23/data/listings.csv.gz",
                   "reviews":"https://data.insideairbnb.com/czech-republic/prague/prague/2025-09-23/data/reviews.csv.gz"},
        "Oslo": {"listings":"https://data.insideairbnb.com/norway/oslo/oslo/2025-09-29/data/listings.csv.gz",
                 "reviews":"https://data.insideairbnb.com/norway/oslo/oslo/2025-09-29/data/reviews.csv.gz"},
        "Copenhagen": {"listings":"https://data.insideairbnb.com/denmark/hovedstaden/copenhagen/2025-09-29/data/listings.csv.gz",
                        "reviews":"https://data.insideairbnb.com/denmark/hovedstaden/copenhagen/2025-09-29/data/reviews.csv.gz"},
        "Stockholm": {"listings":"https://data.insideairbnb.com/sweden/stockholms-l%C3%A4n/stockholm/2025-09-29/data/listings.csv.gz",
                      "reviews":"https://data.insideairbnb.com/sweden/stockholms-l%C3%A4n/stockholm/2025-09-29/data/reviews.csv.gz"}
    }

    dataset = generate_dataset_multiple_cities(city_data, num_properties_per_city=150)
    
    with open("LargeB&B_Dataset.json","w",encoding="utf-8") as f:
        json.dump(dataset,f,indent=2,ensure_ascii=False)
    print("Dataset created")

if __name__ == "__main__":
    main()
