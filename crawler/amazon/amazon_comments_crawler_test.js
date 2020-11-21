const puppeteer = require('puppeteer');
const qs = require('qs');
const fs = require('fs');
const uuid = require('uuid');
const config = require('../config');

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    slowMo: 250 // slow down by 250ms
  });
  const page = await browser.newPage();

  const keyword = config.KEYWORD;
  const MAX_COMMENTS = config.MAX_COMMENTS;

  const data_file = `data_amazon_${encodeURIComponent(keyword)}.json`;
  const output_file = `reviews_amazon_${encodeURIComponent(keyword)}.json`;
  
  const data = JSON.parse(fs.readFileSync(data_file));

  const extractReviews = () => {
    const items = [];
    document.querySelectorAll('.reviewText span').forEach(
      item => {
        if (item) items.push({
          text: item.textContent
        });  
      })
    return items;
  }

  const reviews = []
  for (let i = 0; i < data.length; i++) {
    const item = data[i];
    const product_url = `https://amazon.sg${item.link}`

    await page.goto(product_url);

    reviews.push(...(await page.evaluate(extractReviews))
      .map(item => ({
        ...item, 
        id: uuid.v4(),
      })));

    fs.writeFileSync(output_file, JSON.stringify(reviews));

    if (reviews.length > MAX_COMMENTS) break;
  }

  await browser.close();
})()