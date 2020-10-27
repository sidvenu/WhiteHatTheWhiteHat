from app_store_scraper import AppStore
import json


def normalize_review(review: dict):
    review["text"] = review.pop("review")
    review["score"] = review.pop("rating")
    review["date"] = review["date"].timestamp()
    review["id"] = f"{review['date']}-{review['userName']}"
    return review


def scrape_data():
    app_info = AppStore(app_name="WhiteHat Jr: Online Coding", country="in")
    app_info.review(how_many=3000)
    reviews = list(map(lambda review: normalize_review(review), app_info.reviews))
    f = open("../app-store-reviews.json", "w")
    f.write(json.dumps(reviews))
    f.close()


if __name__ == '__main__':
    scrape_data()
