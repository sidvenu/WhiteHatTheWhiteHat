# WhiteHatTheWhiteHat

I wrote this tool to analyse the allegations of fake reviews against WhiteHat Jr. Though the `*.json` files present in this repo right now are concerned with WhiteHat Jr's app, this tool can be employed to check other apps as well.

## Structure

It consists of a `scraper`, which pulls in the reviews data from Google Play Store and stores it in [reviews.json](reviews.json)
, and `analysis`, which analyses the similarity of reviews and stores the results in 3 files - [groups.json](analysis/groups.json), [low_probability_fakes.json](analysis/low_probability_fakes.json) and [high_probability_fakes.json](analysis/high_probability_fakes.json). Currently, all of the previously linked files contains the analysis of [WhiteHat Jr.'s app](https://play.google.com/store/apps/details?id=com.whitehatjr).

### [groups.json](analysis/groups.json)

This file has a JSON 'Array of Arrays', with each element in the root array representing a 'group'. This grouping is done on the basis of 'similarity'.

### [low_probability_fakes.json](analysis/low_probability_fakes.json)

This file is a filter from groups.json, having 20+ similar reviews in each 'group'. Since this can contain reviews like "Good App" that many people actually type, this is a list of 'low probability' fake reviews.

### [high_probability_fakes.json](analysis/high_probability_fakes.json)

This file is a filter from groups.json, having 2 or more similar reviews in each 'group' and each group containing 10+ words. Since this contains only 'long reviews' that are matching, this is a list of 'high probability' fake reviews.

## Analysis of com.whitehatjr

They seem to have 67 high probability fake reviews, and 1567 low probability fake reviews.

Their high probability fake reviews has the following 'similarity group' sizes:

`[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2]`

Their low probability fake reviews has the following 'similarity group' sizes:

`[145, 215, 114, 28, 26, 33, 24, 63, 52, 55, 65, 392, 27, 46, 21, 60, 29, 24, 48, 24, 36, 40]`

Note:
- Similarity Group - a group of similar reviews
- 'similarity group' sizes - list of sizes of similarity groups.

## How is similarity computed?

This tool currently uses the [TF-IDF cosine similarity](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) as the similarity score of two reviews. If similarity score of two reviews is above the `similarity_threshold`, which is currently defined to be `0.8`, then they are put together in the same group.

## Disclaimer

This tool and the analysis of WhiteHat Jr.'s app was made for educational purposes only. The analysis/findings given above is not to be taken as the truth, and may have errors of its own. Each reader of the above findings is solely responsible for their derived conclusions and subsequent actions, and the author (Siddharth Venu) cannot be held liable for the same.
