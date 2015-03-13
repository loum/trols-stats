<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>North Eastern Junior Tennis</title>
<link rel="stylesheet" type="text/css" href="/styles/style2.css">
<link rel="stylesheet" type="text/css" href="/styles/style.css">
<link rel="stylesheet" type="text/css" href="/js/tinybox2/style.css">
<script language="JavaScript" type="text/javaScript" src="/js/result.js"></script>
<script language="JavaScript" type="text/javaScript" src="/js/tinybox2/tinybox.js"></script>
</head>
<body>
<table align="center" width="740">
  <tr>
    <td>
      <img src="images/logo.png" alt="logo"/>
    </td>
    <td>
      <div class=page-tabs>
        <table cellspacing=0 cellpadding=0>
          <tr valign=top>
            <td class=off>
              <div class=tab>
                <a href="index.php">North Eastern  Junior Tennis</a>
              </div>
            </td>
            <td class=off>
              <div class=tab>
                <a href="clubs.php">Clubs</a>
              </div>
            </td>
            <td class=off>
              <div class=tab>
                <a href="ladders.php">Ladders</a>
              </div>
            </td>
            <td class=on>
              <div class=tab>
                <a href="results.php">Results</a>
              </div>
            </td>
            <td class=off>
              <div class=tab>
                <a href="fixture.php">Fixtures</a>
              </div>
            </td>
            <td class=off>
              <div class=tab>
                <a href="#" onclick="window.open('s_start.php','Club_Zone','toolbar=no,location=no,directories=no,status=no, menubar=no,resizable=yes,copyhistory=no,scrollbars=yes, scrolling=yes,width=800,height=590');return false;">Club Zone</a>
              </div>
            </td>
            <td class=off>
              <div class=tab>
                <a href="p_results.php">Past Seasons</a>
              </div>
            </td>
            <td class="empty">&nbsp;</td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2" class="bar-green-dark">Results</td>
    </tr>
    <tr>
      <td colspan="2">
        <form name="select" id="select" method="POST" action="/nejta/results.php">
          <input type=hidden id="which" name="which"/>
          <input type=hidden id="style" name="style" value=""/>
          <table style="width:720">
            <tr>
              <td style="width:280">
                <label for="daytime">Select a Competition:</label>
                <br/>
                <select id="daytime" name="daytime" Onchange="select_submit(select,0);">
                  <option value="AA" selected>Saturday AM - Autumn 2015</option>
                </select>
              </td>
              <td>
                <br/>
                <span style="color:purple"><b>Results Loaded: </b>9th March 15 @ 02:56:37 PM</span>
              </td>
            </tr>
            <tr>
              <td>
                <label for="section">Select Section:</label>
                <br/>
                <select id="section" name="section" Onchange="select_submit(select,1);">
                  <option value="">&nbsp;</option>
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
                  <option value="AA039" selected>GIRLS 14</option>
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
              <td>
                <br/>
                <span style="color:purple">Click Home Team to Display Match details</span>
              </td>
            </tr>
          </table>
        </form>
        <hr size="1">
          <table align="center">
            <tr>
              <td colspan="9" align="left" class="sb">
                <b>
                  <span class="mg">
                    <a href="ladders.php?daytime=AA&amp;section=AA039&amp;style=">GIRLS 14</a>
                  </span>
                  <br/>31 Jan 15&nbsp;&nbsp;Rd.1
                </b>
                <br/>
              </td>
            </tr>
            <tr>
              <th style="text-align:left;width:250">Home Team</th>
              <th style="text-align:right;width:30">Pts&nbsp;</th>
              <th>S</th>
              <th style="text-align:right;width:20">G</th>
              <th>&nbsp;</th>
              <th style="text-align:right;width:30">Pts&nbsp;</th>
              <th>S</th><th style="text-align:right;width:20">G</th>
              <th style="text-align:left;width:250">&nbsp;Away Team</th>
            </tr>
            <tr valign="middle">
              <td>
                <a onClick="open_match(event,'','AA039011');">Bundoora</a>
              </td>
              <td align="right">8.0&nbsp;</td>
              <td align="right">4</td>
              <td align="right">24</td>
              <td></td>
              <td align="right">0.0&nbsp;</td>
              <td align="right">0</td>
              <td align="right">3</td>
              <td>&nbsp;Barry Road</td>
            </tr>
            <tr>
          <td>Mill Park</td>
          <td colspan=7>&nbsp;</td>
          <td>&nbsp;<font color="#003399">Bye</font></td>
        </tr>
        <tr valign="middle">
          <td><a onClick="open_match(event,'','AA039013');">St Marys</a></td>
          <td align="right">8.0&nbsp;</td>
          <td align="right">4</td>
          <td align="right">24</td>
          <td></td>
          <td align="right">0.0&nbsp;</td>
          <td align="right">0</td>
          <td align="right">8</td>
          <td>&nbsp;Watsonia&nbsp;
            <span style="color:blue">Blue</span>
          </td>
        </tr>
        <tr valign="middle">
          <td><a onClick="open_match(event,'','AA039014');">Watsonia&nbsp;<span style="color:red">Red</span></a></td>
          <td align="right">6.0&nbsp;</td>
          <td align="right">2</td>
          <td align="right">20</td>
          <td></td>
          <td align="right">2.0&nbsp;</td>
          <td align="right">2</td>
          <td align="right">16</td>
          <td>&nbsp;View Bank</td>
        </tr>
        <tr>
          <td>
            <br/>
          </td>
        </tr>
        <tr>
          <td colspan="9" align="left" class="sb"><b>7 Feb 15&nbsp;&nbsp;Rd.2</b><br/></td>
        </tr>
        <tr>
          <th style="text-align:left;width:250">Home Team</th>
          <th style="text-align:right;width:30">Pts&nbsp;</th>
          <th>S</th>
          <th style="text-align:right;width:20">G</th>
          <th>&nbsp;</th><th style="text-align:right;width:30">Pts&nbsp;</th>
          <th>S</th><th style="text-align:right;width:20">G</th>
          <th style="text-align:left;width:250">&nbsp;Away Team</th>
        </tr>
        <tr>
          <td><font color="#003399">Bye</font></td>
          <td colspan=7>&nbsp;</td>
          <td>&nbsp;St Marys</td>
        </tr>
        <tr valign="middle">
          <td><a onClick="open_match(event,'','AA039022');">Barry Road</a></td>
          <td align="right">8.0&nbsp;</td>
          <td align="right">4</td>
          <td align="right">24</td>
          <td></td>
          <td align="right">0.0&nbsp;</td>
          <td align="right">0</td>
          <td align="right">12</td>
          <td>&nbsp;Mill Park</td>
        </tr>
        <tr valign="middle">
          <td><a onClick="open_match(event,'','AA039023');">View Bank</a></td>
          <td align="right">1.0&nbsp;</td>
          <td align="right">1</td>
          <td align="right">14</td>
          <td></td>
          <td align="right">7.0&nbsp;</td>
          <td align="right">3</td>
          <td align="right">22</td>
          <td>&nbsp;Bundoora</td>
        </tr>
        <tr valign="middle">
          <td><a onClick="open_match(event,'','AA039024');">Watsonia&nbsp;<span style="color:blue">Blue</span></a></td>
          <td align="right">2.0&nbsp;</td>
          <td align="right">2</td>
          <td align="right">14</td>
          <td></td>
          <td align="right">6.0&nbsp;</td>
          <td align="right">2</td>
          <td align="right">18</td>
          <td>&nbsp;Watsonia&nbsp;<span style="color:red">Red</span></td>
        </tr>
        <tr>
          <td>
            <br/>
          </td>
        </tr>
        <tr>
          <td colspan="9" align="left" class="sb"><b>14 Feb 15&nbsp;&nbsp;Rd.3</b>
            <br/>
          </td>
        </tr>
        <tr>
          <th style="text-align:left;width:250">Home Team</th>
          <th style="text-align:right;width:30">Pts&nbsp;</th>
          <th>S</th><th style="text-align:right;width:20">G</th>
          <th>&nbsp;</th>
          <th style="text-align:right;width:30">Pts&nbsp;</th>
          <th>S</th>
          <th style="text-align:right;width:20">G</th>
          <th style="text-align:left;width:250">&nbsp;Away Team</th>
        </tr>
        <tr>
          <td>Bundoora</td>
          <td colspan=7 align=center class=sg>Wash Out</td>
          <td>&nbsp;Watsonia&nbsp;<span style="color:blue">Blue</span></td>
        </tr>
        <tr>
          <td>Barry Road</td>
          <td colspan=7 align=center class=sg>Wash Out</td>
          <td>&nbsp;View Bank</td>
        </tr>
        <tr>
          <td>St Marys</td>
          <td colspan=7 align=center class=sg>Wash Out</td>
          <td>&nbsp;Mill Park</td>
        </tr>
        <tr>
          <td>Watsonia&nbsp;<span style="color:red">Red</span></td>
          <td colspan=7>&nbsp;</td>
          <td>&nbsp;<font color="#003399">Bye</font></td>
        </tr>
        <tr>
          <td>
            <br/>
          </td>
        </tr>
        <tr>
          <td colspan="9" align="left" class="sb"><b>21 Feb 15&nbsp;&nbsp;Rd.4</b><br/></td>
        </tr>
        <tr>
          <th style="text-align:left;width:250">Home Team</th>
          <th style="text-align:right;width:30">Pts&nbsp;</th>
          <th>S</th>
          <th style="text-align:right;width:20">G</th>
          <th>&nbsp;</th>
          <th style="text-align:right;width:30">Pts&nbsp;</th>
          <th>S</th>
          <th style="text-align:right;width:20">G</th>
          <th style="text-align:left;width:250">&nbsp;Away Team</th>
        </tr>
        <tr>
          <td><font color="#003399">Bye</font></td>
          <td colspan=7>&nbsp;</td>
          <td>&nbsp;Bundoora</td>
        </tr>
        <tr valign="middle">
          <td><a onClick="open_match(event,'','AA039042');">Mill Park</a></td>
          <td align="right">1.5&nbsp;</td>
          <td align="right">1</td>
          <td align="right">14</td><td></td>
          <td align="right">6.5&nbsp;</td>
          <td align="right">2</td>
          <td align="right">21</td><td>&nbsp;Watsonia&nbsp;<span style="color:red">Red</span></td>
        </tr>
        <tr valign="middle">
          <td><a onClick="open_match(event,'','AA039043');">St Marys</a></td>
          <td align="right">7.0&nbsp;</td>
          <td align="right">3</td>
          <td align="right">18</td><td></td>
          <td align="right">1.0&nbsp;</td>
          <td align="right">1</td>
          <td align="right">17</td>
          <td>&nbsp;Barry Road</td>
        </tr>
        <tr valign="middle">
          <td><a onClick="open_match(event,'','AA039044');">Watsonia&nbsp;<span style="color:blue">Blue</span></a></td>
          <td align="right">7.0&nbsp;</td>
          <td align="right">3</td>
          <td align="right">18</td><td></td>
          <td align="right">1.0&nbsp;</td>
          <td align="right">1</td>
          <td align="right">14</td><td>&nbsp;View Bank</td>
        </tr>
        <tr>
          <td>
            <br/>
          </td>
        </tr>
        <tr>
          <td colspan="9" align="left" class="sb"><b>28 Feb 15&nbsp;&nbsp;Rd.5</b><br/></td>
        </tr>
        <tr>
          <th style="text-align:left;width:250">Home Team</th>
          <th style="text-align:right;width:30">Pts&nbsp;</th>
          <th>S</th><th style="text-align:right;width:20">G</th>
          <th>&nbsp;</th>
          <th style="text-align:right;width:30">Pts&nbsp;</th>
          <th>S</th><th style="text-align:right;width:20">G</th>
          <th style="text-align:left;width:250">&nbsp;Away Team</th>
        </tr>
        <tr valign="middle">
          <td><a onClick="open_match(event,'','AA039051');">Bundoora</a></td>
          <td align="right">7.0&nbsp;</td>
          <td align="right">3</td>
          <td align="right">21</td><td></td>
          <td align="right">1.0&nbsp;</td>
          <td align="right">1</td>
          <td align="right">13</td>
          <td>&nbsp;Mill Park</td>
        </tr>
        <tr>
          <td>Barry Road</td>
          <td colspan=7 align=center class=sg>Wash Out</td>
          <td>&nbsp;Watsonia&nbsp;<span style="color:blue">Blue</span></td>
        </tr>
        <tr>
          <td>View Bank</td>
          <td colspan=7>&nbsp;</td>
          <td>&nbsp;<font color="#003399">Bye</font></td></tr>
        <tr valign="middle">
          <td><a onClick="open_match(event,'','AA039054');">Watsonia&nbsp;<span style="color:red">Red</span></a></td>
          <td align="right">0.0&nbsp;</td>
          <td align="right">0</td>
          <td align="right">11</td><td></td>
          <td align="right">8.0&nbsp;</td>
          <td align="right">4</td>
          <td align="right">24</td><td>&nbsp;St Marys</td>
        </tr>
        <tr>
          <td>
            <br/>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
<center><img src="images/tennis_line.gif" width=488 height=42 align=middle alt="footer" /></center>
</body></html>
