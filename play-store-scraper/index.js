const gplay = require('google-play-scraper');
const fs = require("fs");
const stdio = require('stdio');

const args = stdio.getopt({
    'appId': { args: 1, key: 'a', description: 'Application ID to get reviews for' }
});

gplay.reviews({
    appId: args.appId,
    sort: gplay.sort.RATING,
    num: 100000
}).then((data) => {
    fs.writeFileSync("../play-store-reviews.json", JSON.stringify(data), "utf-8");
});
