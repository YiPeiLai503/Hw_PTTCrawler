# Hw_PTTCrawler

程式說明:
<br>使用程式爬取PTT表特版前一天的所有文章，並記錄以下資訊:</br>
        <br>1. 作者帳號</br>
        <br>2. 文章標題</br>
        <br>3. 發文時間</br>
        <br>4. 發文IP</br>
        <br>5. 文章中第一張圖片網址</br>
        <br>6. 該文章推數</br>
        <br>7. 該文章噓數</br>
    <br>假如文章中不存在圖片，則不紀錄，最後將以上資訊以及爬取時間以文字檔方式儲存，格式為.csv</br>
<br></br>
<br>crawlerTimeSet:</br>
　　<br>時間計算方式為 今天 - 設定值，假如設定值為 0 ，則日期為今天，以此列推。</br>
　　<br>預設為爬取一天的文章，故startValue為 1，stopValue為 2。</br>　　
　　<br>PTT上日期格是為 月/日，故建立此物件後，呼叫crawlerTime會回傳符合此格式的起始值與終止值。</br>
<br></br>　　
  　<br>getValue:　可取得現在設定的值。</br>
  　<br>setValue:　需要兩個傳入值，一個是開始，一個是結束。</br>
　　<br>crawlerTime:　回傳值為與PTT上格式相同的日期，第一個為起始時間，第二個為終止時間</br>
<br></br>
<br>crawlerWeb:</br>
　　<br>setWeb: 用來更改爬取之目標網站</br>
　　<br>getCertified: 用來取得PTT的18歲驗證</br>
　　<br>getSoup: 取得經過18歲驗證後，網頁之html碼</br>
　　<br>getNextPage:　PTT顯示為最新文章，因此會在最後一頁，透過此方法能取得上一頁的link</br>
　　<br>getArticleUrl:　需給予起始與結束的日期，可透過crawlerTimeSet的crawlerTime回傳值得到。回傳值為符合條件之所有文章link。</br>
<br></br>
<br>retrieveInformation:</br>
　　<br>getIP:　回傳值為發表文章作者之IP</br>
  　<br>getPIC:　回傳值為文章中的第一張圖片link</br>
　　<br>count:　回傳值為文章中的「推」和「噓」的數量</br>
　　<br>retrieveMain:　回傳值為list，內容包含爬蟲爬取時間、作者名稱、文章標題、文章發表日期、作者IP、第一張圖片link、推的數量、噓的數量</br>
<br></br>
<br>if__name__=='__main__':</br>
　　<br>建立crawlerTimeSet物件</br>
  　<br>建立crawlerWeb物件</br>
　　<br>建立retrieveInformation物件</br>
    <br>allInform 用來儲存 retrieveInformation.retrieveMain回傳之物件，使其成為二維陣列</br>
    因在過程中發現不明原因產生之None值，在寫入csv時會產生Error，因此在寫入前先進行一次filter</br>
