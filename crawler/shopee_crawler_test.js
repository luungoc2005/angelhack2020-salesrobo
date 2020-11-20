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
  await page.goto(`https://shopee.sg/search?${qs.stringify({
    keyword: encodeURIComponent(keyword),
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

  await page.waitForSelector(".shopee-mini-page-controller__state");
  const maxPage = await page.evaluate(() => {
    const containerElement = document.querySelector(".shopee-mini-page-controller__state");
    const pageNavLinks = containerElement.children;
    const numberedPages = []
    pageNavLinks.forEach(element => 
      numberedPages.push(parseInt(element.textContent)))
    return Math.max(...numberedPages);
  });

  let i = 0; // starts from 1
  const items = (await page.evaluate(extractItems))
    .map(item => ({id: uuid.v4(), ...item}));
  while (i < maxPage && items.length < MAX_ITEMS) {
    i += 1;
    await page.goto(`https://shopee.sg/search?${qs.stringify({
      keyword: encodeURIComponent(keyword),
      page: i,
    })}`);
    await page.waitForSelector(".shopee-mini-page-controller__state");
    items.push(...(await page.evaluate(extractItems))
      .map(item => ({id: uuid.v4(), ...item})));
    
    // write every time
    fs.writeFileSync(`data_shopee_${keyword}.json`, JSON.stringify(items));  
  }

  // let items = [];
  // try {
  //   let previousHeight;
  //   let newItems = [];
  //   while (true) {
  //     newItems = await page.evaluate(extractItems);
  //     if (newItems.length > items.length) {
  //       items = newItems;
  //       previousHeight = await page.evaluate('document.body.scrollHeight');
  //       await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
  //       await page.waitForFunction(`document.body.scrollHeight > ${previousHeight}`);
  //       await page.waitForTimeout(500);
  //     }
  //     else {
  //       break;
  //     }
  //   }
  // }
  // catch (e) {}
  // console.log(items);
  // console.log(items.length);

  await browser.close();
})();
