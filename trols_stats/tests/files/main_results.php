<html>
  <head>
    <title>North Eastern Junior Tennis</title>
    <link rel="stylesheet" type="text/css" href="/styles/style2.css"/>
    <link rel="stylesheet" type="text/css" href="/styles/style.css"/>
    <link rel="stylesheet" type="text/css" href="/js/tinybox2/style.css"/>
    <script language="JavaScript" type="text/javaScript" src="/js/result.js"/>
    <script language="JavaScript" type="text/javaScript" src="/js/tinybox2/tinybox.js"/>
  </head>
  <body>
    <table align="center" width="740">
      <tr>
        <td>
          <img src="images/logo.png" alt="logo"/>
        </td>
        <td>
          <div class="page-tabs">
            <table cellspacing="0" cellpadding="0">
              <tr valign="top">
                <td class="off">
                  <div class="tab">
                    <a href="index.php">North Eastern  Junior Tennis</a>
                  </div>
                </td>
                <td class="off">
                  <div class="tab">
                    <a href="clubs.php">Clubs</a>
                  </div>
                </td>
                <td class="off">
                  <div class="tab">
                    <a href="ladders.php">Ladders</a>
                  </div>
                </td>
                <td class="on">
                  <div class="tab">
                    <a href="results.php">Results</a>
                  </div>
                </td>
                <td class="off">
                  <div class="tab">
                    <a href="fixture.php">Fixtures</a>
                  </div>
                </td>
                <td class="off">
                  <div class="tab">
                    <a href="#" onclick="window.open('s_start.php','Club_Zone','toolbar=no,location=no,directories=no,status=no, menubar=no,resizable=yes,copyhistory=no,scrollbars=yes, scrolling=yes,width=800,height=590');return false;">Club Zone</a>
                  </div>
                </td>
                <td class="off">
                  <div class="tab">
                    <a href="p_results.php">Past Seasons</a>
                  </div>
                </td>
                <td class="empty">&#160;</td>
              </tr>
            </table>
          </div>
        </td>
      </tr>
      <tr>
        <td colspan="2" class="bar-green-dark">Results</td>
      </tr>
      <tr>
        <td colspan="2">
          <form name="select" id="select" method="POST" action="/nejta/results.php">
            <input type="hidden" id="which" name="which"/>
            <input type="hidden" id="style" name="style" value=""/>
            <table style="width:720">
              <tr>
                <td style="width:280">
                  <label for="daytime">Select a Competition:</label>
                  <br/>
                  <select id="daytime" name="daytime" onchange="select_submit(select,0);">
                    <option value="AA" selected="selected">Saturday AM - Autumn 2015</option>
                  </select>
                </td>
                <td>
                  <br/>
                  <span style="color:purple"><b>Results Loaded: </b>21st April 15 @ 09:55:18 PM</span>
                </td>
              </tr>
              <tr>
                <td>
                  <label for="section">Select Section:</label>
                  <br/>
                  <select id="section" name="section" onchange="select_submit(select,1);">
                    <option value="">&#160;</option>
                    <option value="AA026">GIRLS 1</option>
                    <option value="AA027">GIRLS 2</option>
                    <option value="AA028">GIRLS 3</option>
                    <option value="AA029">GIRLS 4</option>
                    <option value="AA030">GIRLS 5</option>
                    <option value="AA031">GIRLS 6</option>
                    <option value="AA032">GIRLS 7</option>
                    <option value="AA033">GIRLS 8</option>
                    <option value="AA034">GIRLS 9</option>
                    <option value="AA035">GIRLS 10</option>
                    <option value="AA036">GIRLS 11</option>
                    <option value="AA037">GIRLS 12</option>
                    <option value="AA038">GIRLS 13</option>
                    <option value="AA039">GIRLS 14</option>
                    <option value="AA040">GIRLS 15</option>
                    <option value="AA001">BOYS 1</option>
                    <option value="AA002">BOYS 2</option>
                    <option value="AA003">BOYS 3</option>
                    <option value="AA004">BOYS 4</option>
                    <option value="AA005">BOYS 5</option>
                    <option value="AA006">BOYS 6</option>
                    <option value="AA007">BOYS 7</option>
                    <option value="AA008">BOYS 8</option>
                    <option value="AA009">BOYS 9</option>
                    <option value="AA010">BOYS 10</option>
                    <option value="AA011">BOYS 11</option>
                    <option value="AA012">BOYS 12</option>
                    <option value="AA013">BOYS 13</option>
                    <option value="AA014">BOYS 14</option>
                    <option value="AA015">BOYS 15</option>
                    <option value="AA016">BOYS 16</option>
                    <option value="AA017">BOYS 17</option>
                    <option value="AA018">BOYS 18</option>
                    <option value="AA019">BOYS 19</option>
                    <option value="AA020">BOYS 20</option>
                    <option value="AA021">BOYS 21</option>
                    <option value="AA022">BOYS 22</option>
                    <option value="AA023">BOYS 23</option>
                    <option value="AA024">BOYS 24</option>
                    <option value="AA025">BOYS 25</option>
                  </select>
                </td>
              </tr>
            </table>
          </form>
        </td>
      </tr>
    </table>
    <center>
      <img src="images/tennis_line.gif" width="488" height="42" align="middle" alt="footer"/>
    </center>
  </body>
</html>
