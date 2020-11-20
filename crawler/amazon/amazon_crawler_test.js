const puppeteer = require('puppeteer');
const qs = require('qs');
const fs = require('fs');
const uuid = require('uuid');

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    slowMo: 250 // slow down by 250ms
  });
  const page = await browser.newPage();

  const keyword = 'smartphone';
  const MAX_ITEMS = 500;

  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  await page.goto(`https://amazon.sg/s?${qs.stringify({
    k: encodeURIComponent(keyword),
  })}`);

  const extractItems = () => {
    const elements = document.querySelectorAll('.s-result-item');
    if (!elements.length) return [];

    const items = [];
    for (let i = 0; i < elements.length; i++) {
      if (!elements[i] || !elements[i].querySelector('a.a-link-normal.a-text-normal > span')) continue;

      // get price
      const priceWholeElement = elements[i].querySelector('span.a-price-whole')
      const priceFractionElement = elements[i].querySelector('span.a-price-fraction')
      const price = parseFloat(`${priceWholeElement ? priceWholeElement.textContent.replace(",", "") : '0'}.${priceFractionElement ? priceFractionElement.textContent : '0'}`)
      
      // get sold (number of reviews)

      const numReviewsElement = elements[i].querySelector('div.a-section div.a-size-small span.a-size-base')
      const sold = parseInt(numReviewsElement ? numReviewsElement.textContent.replace(",", "") : 0)

      items.push({
        image: elements[i].querySelector('img').getAttribute('src'),
        link: elements[i].querySelector('a.a-link-normal.a-text-normal').getAttribute('href'),
        name: elements[i].querySelector('a.a-link-normal.a-text-normal > span').textContent,
        price,
        sold,
        rating: -1,
      });
    }

    return items;
  }

  await page.waitForSelector("ul.a-pagination");
  const maxPage = await page.evaluate(() => {
    const containerElement = document.querySelector("ul.a-pagination");
    const pageNavLinks = [...containerElement.children];
    const numberedPages = []
    for (let i = 0; i < pageNavLinks.length; i++) {
      const element = pageNavLinks[i];
      numberedPages.push(parseInt(element.textContent));
    }
    return Math.max(...numberedPages.filter(it => !isNaN(it)));
  });
  console.log(`MAX PAGE: ${maxPage}`)

  let i = 1; // starts from 1
  const items = (await page.evaluate(extractItems))
    .map(item => ({id: uuid.v4(), ...item}));
  while (i < maxPage && items.length < MAX_ITEMS) {
    i += 1;
    await page.goto(`https://amazon.sg/s?${qs.stringify({
      k: encodeURIComponent(keyword),
      page: i,
    })}`);
    await page.waitForSelector("ul.a-pagination");
    items.push(...(await page.evaluate(extractItems))
      .map(item => ({id: uuid.v4(), ...item})));
    
    // write every time
    fs.writeFileSync(`data_amazon_${keyword}.json`, JSON.stringify(items));  
  }

  await browser.close();
})();
