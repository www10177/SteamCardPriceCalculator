# SteamCardPriceCalculator

## Introduction  
就是一個簡單協助計算steam合卡收益的小工具，卡片資料來源[steamcardexchange](https://www.steamcardexchange.net)，卡片價格為即時從steam上爬取，但因steam api有一分鐘內存取次數的限制，使用太多的話可能會出現錯誤/價格皆為-1，稍待幾分鐘後應可恢復

## Problems  
 - [ ] 多次查詢後會被steam api 暫停，稍待幾分鐘後應可恢復
 - [ ] 目前暫不查詢閃卡價格，故閃卡價格皆為-1

## Usage :
  1. 下載[web.zip](https://github.com/www10177/SteamCardPriceCalculator/releases/)
  2. 解壓，執行 `web.exe`
  3. 打開瀏覽器，網址列輸入`localhost` 或 `http://127.0.0.1`
