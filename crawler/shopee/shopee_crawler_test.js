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
  const MAX_ITEMS = config.MAX_ITEMS;

  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  await page.goto(`https://shopee.sg/search?${qs.stringify({
    keyword,
  })}`);

  const extractItems = () => {
    const elements = document.querySelectorAll('div[data-sqe="item"]');
    if (!elements.length) return [];

    const items = [];
    for (let i = 0; i < elements.length; i++) {
      if (!elements[i] || !elements[i].querySelector('div[data-sqe="name"]')) continue;
      const contentContainer = elements[i].querySelector('div[data-sqe="name"]').parentElement;
      const directChildren = contentContainer.children;
      let price = -1;
      let sold = -1;
      for (let a = 0; a < directChildren.length; a++) {
        if (directChildren[a].textContent.indexOf("$")) {
          // price
          // take last element
          const priceElements = directChildren[a].children;
          price = parseFloat(priceElements[priceElements.length - 1].textContent)
        }
        else if (directChildren[a].textContent.indexOf("sold") > -1) {
          // number sold & rating
          const ratingSoldChildren = directChildren[a].children;
          for (let b = 0; b < ratingSoldChildren.length; b++) {
            if (ratingSoldChildren[b].textContent.indexOf("sold") > -1) {
              sold = parseInt(directChildren[a].textContent);
            }
            break;
          }
        }
      }
      const starsContainer = elements[i].querySelector('.shopee-rating-stars')
      const goldStars = starsContainer ? starsContainer.querySelectorAll('.shopee-rating-stars__gold-star').length : -1
      items.push({
        image: elements[i].querySelector('img').getAttribute('src'),
        link: elements[i].querySelector('a').getAttribute('href'),
        name: elements[i].querySelector('div[data-sqe="name"]').textContent,
        price,
        sold,
        rating: goldStars,
      });
    }

    return items;
  }

  let maxPage = 1;
  try {
    await page.waitForSelector(".shopee-mini-page-controller__state");  
    maxPage = await page.evaluate(() => {
      const containerElement = document.querySelector(".shopee-mini-page-controller__state");
      const pageNavLinks = [...containerElement.children];
      const numberedPages = []
      for (let i = 0; i < pageNavLinks.length; i++) {
        const element = pageNavLinks[i];
        numberedPages.push(parseInt(element.textContent));
      }
      return Math.max(...numberedPages.filter(it => !isNaN(it)));
    });
  }
  catch {}

  let i = 0; // starts from 1
  const items = (await page.evaluate(extractItems))
    .map(item => ({id: uuid.v4(), ...item}));
  fs.writeFileSync(`data_shopee_${encodeURIComponent(keyword)}.json`, JSON.stringify(items));
  while (i < maxPage - 1 && items.length < MAX_ITEMS) {
    i += 1;
    await page.goto(`https://shopee.sg/search?${qs.stringify({
      keyword,
      page: i,
    })}`);
    await page.waitForSelector(".shopee-mini-page-controller__state");
    items.push(...(await page.evaluate(extractItems))
      .map(item => ({id: uuid.v4(), ...item})));
    
    // write every time
    fs.writeFileSync(`data_shopee_${encodeURIComponent(keyword)}.json`, JSON.stringify(items));  
  }

  await browser.close();
})();
