const puppeteer = require('puppeteer');
const qs = require('qs');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    slowMo: 250 // slow down by 250ms
  });
  const page = await browser.newPage();
  const keyword = 'smartphone';

  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  await page.goto(`https://www.lazada.sg/catalog/?${qs.stringify({
    q: encodeURIComponent(keyword),
  })}`);

  // await page.waitForSelector('input[type="search"]');
  // await page.$eval('input[type="search"]', 
  //   el => el.value = "smartphone");

  // await page.click('button[data-spm-click="gostr=/lzdpub.header.search;locaid=d_go"]');
  // await page.waitForNavigation({
  //   waitUntil: "networkidle2",
  // })

  // await page.screenshot({ path: 'screenshot.png' });

  const extractItems = () => {
    const elements = document.querySelectorAll('div[data-qa-locator="product-item"]');
    if (!elements.length) return [];

    const items = [];
    for (let i = 0; i < elements.length; i++) {
      items.push({
        link: elements[i].querySelector('a').getAttribute('href'),
        name: elements[i].querySelector('img').getAttribute('alt'),
      })
    }
  }

  page.$eval(".ant-pagination", async (containerElement) => {
    const pageNavLinks = containerElement.querySelectorAll('a');
    const numberedPages = []
    pageNavLinks.forEach(element => {
      if (element.getAttribute('href'))
        numberedPages.push(parseInt(element.textContent))
    })
    const maxPage = Math.max(...numberedPages);

    let i = 1;
    let items = await page.evaluate(extractItems);
    while (i < maxPage && items.length < 100) {
      i += 1;
      await page.goto(`https://www.lazada.sg/catalog/?${qs.stringify({
        q: encodeURIComponent(keyword),
        page: i,
      })}`);
      items.push(...await page.evaluate(extractItems));
    }

    fs.writeFileSync('data.json', JSON.stringify(items));
  });



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

  // await browser.close();
})();
