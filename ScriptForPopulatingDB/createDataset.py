import csv
import json
import random
from datetime import timedelta, datetime
from faker import Faker
import requests
import gzip
import io
import os

# Initialize Faker
fake = Faker()
Faker.seed(42)

# Create output folder
os.makedirs("output_entities", exist_ok=True)

# Helper functions
def generate_customer():
    return {
        "id": fake.uuid4(),
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "optionPreference": {
            "theme": random.choice(["dark", "light"]),
            "language": random.choice(["en", "it", "es", "fr", "de"])
        },
        "phone": fake.phone_number(),
        "methodPayment": {
            "type": random.choice(["credit_card", "paypal"]),
            "provider": fake.credit_card_provider()
        }
    }

def generate_manager():
    return {
        "id": fake.uuid4(),
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "optionPreference": {
            "theme": random.choice(["dark", "light"]),
            "language": random.choice(["en", "it", "es", "fr", "de"])
        },
        "phone": fake.phone_number(),
        "iban": fake.iban()
    }

def generate_reservation():
    check_in = fake.date_between("-30d", "+30d")
    check_out = check_in + timedelta(days=random.randint(1, 7))
    return {
        "id": fake.uuid4(),
        "checkInDate": check_in.isoformat(),
        "checkOutDate": check_out.isoformat(),
        "creationDate": fake.date_between("-60d", check_in).isoformat(),
        "adults": random.randint(1, 4),
        "children": random.randint(0, 2),
        "status": random.choice(["confirmed", "cancelled", "completed"])
    }

# POI coordinates
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

def generate_pois(city, property_id, num_pois=5):
    city_places = famous_places_coords.get(city, [])
    pois = []
    for poi in city_places[:num_pois]:
        pois.append({
            "id": fake.uuid4(),
            "property_id": property_id,
            "name": poi["name"],
            "coordinates": poi["coordinates"],
            "type": random.choice(["historical", "museum", "park", "monument", "landmark"])
        })
    return pois

def download_insideairbnb_csv(file_url):
    try:
        r = requests.get(file_url, timeout=20)
        r.raise_for_status()
        with gzip.open(io.BytesIO(r.content), mode='rt', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
        return reader
    except Exception as e:
        print(f"Error downloading CSV {file_url}: {e}")
        return []

# Dataset generation

def generate_dataset(listings_csv_url, reviews_csv_url, city, entities, max_properties=150):
    listings = download_insideairbnb_csv(listings_csv_url)
    reviews_csv = download_insideairbnb_csv(reviews_csv_url)

    for row in listings[:max_properties]:
        property_id = fake.uuid4()

        amenities = row.get("amenities", "").replace("{","").replace("}","").split(",")
        if amenities == [""]:
            amenities = [fake.word() for _ in range(5)]

        lat = float(row.get("latitude", 0))
        lon = float(row.get("longitude", 0))
        city_name = row.get("city", city)

        # Manager
        manager = generate_manager()
        entities["managers"].append(manager)

        # Property photos (structure)
        property_photos = [fake.image_url() for _ in range(5)]

        # Property
        property_data = {
            "id": property_id,
            "name": row.get("name") or fake.company(),
            "address": row.get("neighbourhood_cleansed") or fake.address(),
            "description": row.get("description") or fake.text(max_nb_chars=500),
            "amenities": amenities,
            "photos": property_photos,
            "email": fake.company_email(),
            "country": row.get("country") or "Unknown",
            "region": row.get("state") or "Unknown",
            "city": city_name,
            "manager_id": manager["id"],
            "coordinates": [lat, lon]
        }
        entities["properties"].append(property_data)

        # Rooms
        rooms_for_property = []
        for i in range(random.randint(3,5)):
            room_photos = [fake.image_url() for _ in range(random.randint(3,5))]
            room = {
                "id": fake.uuid4(),
                "property_id": property_id,
                "roomType": random.choice(["single","matrimonial","double","suite"]),
                "amenities": amenities,
                "name": f"Room {i+1}",
                "beds": random.randint(1,3),
                "photos": room_photos,
                "status": "available",
                "capacityAdults": random.randint(1,4),
                "capacityChildren": random.randint(0,3),
                "pricePerNightAdults": round(random.uniform(30,200),2),
                "pricePerNightChildren": round(random.uniform(10,50),2)
            }
            entities["rooms"].append(room)
            rooms_for_property.append(room)

        # Customers & Reservations & Messages
        for _ in range(random.randint(10,20)):
            customer = generate_customer()
            entities["customers"].append(customer)

            reservation = generate_reservation()
            reservation["room_id"] = random.choice(rooms_for_property)["id"] 
            reservation["customer_id"] = customer["id"]
            entities["reservations"].append(reservation)

            # Generate Messages
            if random.random() > 0.5:
                # 1. Customer sends a message
                msg_time_1 = datetime.fromisoformat(reservation["creationDate"]) + timedelta(minutes=random.randint(10, 120))
                msg1 = {
                    "id": fake.uuid4(),
                    "sender_id": customer["id"],
                    "recipient_id": manager["id"],
                    "timestamp": msg_time_1.isoformat(),
                    "content": fake.sentence(nb_words=10),
                    "is_read": True
                }
                entities["messages"].append(msg1)

                # 2. Manager replies
                msg_time_2 = msg_time_1 + timedelta(minutes=random.randint(5, 60))
                msg2 = {
                    "id": fake.uuid4(),
                    "sender_id": manager["id"],
                    "recipient_id": customer["id"],
                    "timestamp": msg_time_2.isoformat(),
                    "content": fake.sentence(nb_words=12),
                    "is_read": random.choice([True, False])
                }
                entities["messages"].append(msg2)

        # Reviews
        for row_rev in reviews_csv[:50]:
            review = {
                "id": fake.uuid4(),
                "property_id": property_id,
                "creationDate": row_rev.get("date","") or fake.date_between("-1y","today").isoformat(),
                "text": row_rev.get("comments") or fake.text(max_nb_chars=300),
                "rating": random.randint(3,5),
                
                # ---- Nuovi campi aggiunti ----
                "cleanliness": random.randint(3, 5),   # Pulizia
                "communication": random.randint(3, 5), # Comunicazione
                "location": random.randint(3, 5),      # Posizione
                "value": random.randint(3, 5),         # Rapporto qualità/prezzo
                # ------------------------------

                "managerReply": fake.sentence() if random.choice([True,False]) else None
            }
            entities["reviews"].append(review)

        # POIs
        entities.setdefault("pois",[])
        entities["pois"].extend(generate_pois(city_name, property_id))

    return entities

# Main execution

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

    entities = {
        "customers": [],
        "managers": [],
        "properties": [],
        "rooms": [],
        "reservations": [],
        "reviews": [],
        "pois": [],
        "messages": []
    }

    for city, urls in city_data.items():
        print(f"Generating data for {city}...")
        generate_dataset(urls["listings"], urls["reviews"], city, entities, max_properties=150)

    for entity_name, data in entities.items():
        with open(f"output_entities/{entity_name}.json","w",encoding="utf-8") as f:
            json.dump(data,f,indent=2,ensure_ascii=False)

    print("All datasets created successfully.")

if __name__ == "__main__":
    main()