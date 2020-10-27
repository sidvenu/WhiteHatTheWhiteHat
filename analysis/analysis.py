from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import re
import math

from typing import List

similarity_threshold = 0.8
vectorizer = TfidfVectorizer()

reviews_file_name = input("Input the path to reviews file: ")
if reviews_file_name.endswith(".json"):
    reviews_file_name = reviews_file_name[:-5]


def analyze():
    global reviews_file_name

    reviews = json.loads(open(f"{reviews_file_name}.json", "r").read())
    """
    id - Identifier of a review
    text - Review Text
    score - 1-5 star rating
    """
    index_of_review_id = {review_id["id"]: index for index, review_id in enumerate(reviews)}
    review_texts = list(map(lambda x: x["text"].lower(), reviews))
    docs_tfidf = vectorizer.fit_transform(review_texts)
    word_counts = [len(re.findall(r'\w+', review_text)) for review_text in review_texts]
    groups = []
    cur_idx = 0
    for i in range(len(reviews)):
        if i % 200 == 0:
            print(i)
        is_matched = False
        for group_index in range(len(groups)):
            reviews_in_group = groups[group_index]
            if type(reviews_in_group) == list:
                for review_group_index in range(len(reviews_in_group)):
                    review_in_group = reviews_in_group[review_group_index]
                    idx_review_in_group = index_of_review_id[review_in_group["id"]]
                    if not(math.floor(word_counts[i] * 0.75) <= word_counts[idx_review_in_group] <= math.floor(word_counts[i] * 1.33)):
                        break
                    similarity = cosine_similarity(docs_tfidf[i], docs_tfidf[idx_review_in_group])[0][0]
                    if similarity > similarity_threshold:
                        reviews_in_group.append(reviews[i])
                        is_matched = True
                        break
                    if similarity < 0.5:
                        break
            else:
                review_in_group = reviews_in_group
                idx_review_in_group = index_of_review_id[review_in_group["id"]]
                if not(math.floor(word_counts[i] * 0.75) <= word_counts[idx_review_in_group] <= math.floor(word_counts[i] * 1.33)):
                    continue
                similarity = cosine_similarity(docs_tfidf[i], docs_tfidf[idx_review_in_group])[0][0]
                if similarity > similarity_threshold:
                    groups[group_index] = [review_in_group, reviews[i]]
                    is_matched = True
            if is_matched:
                break
        if not is_matched:
            groups.append(reviews[i])
            cur_idx += 1
    f = open(f"{reviews_file_name}-groups.json", "w")
    f.write(json.dumps(groups))
    f.close()


def clean_review_groups(review_groups: List[list]):
    return [list(map(lambda x: x["text"], review_group)) for review_group in review_groups]


def infer():
    groups = json.loads(open(f"{reviews_file_name}-groups.json", "r").read())
    low_probability_fakes = list(filter(lambda g: len(g) > 20, groups))
    high_probability_fakes = list(filter(
        lambda g: type(g) == list and len(g) > 1 and len(re.findall(r'\w+', g[0]["text"])) > 9,
        groups))
    f = open(f"{reviews_file_name}-low-probability-fakes.json", "w")
    f.write(json.dumps(clean_review_groups(low_probability_fakes), indent=2))
    f.close()
    f = open(f"{reviews_file_name}-high-probability-fakes.json", "w")
    f.write(json.dumps(clean_review_groups(high_probability_fakes), indent=2))
    f.close()


analyze()
infer()
