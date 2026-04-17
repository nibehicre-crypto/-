<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta http-equiv="Content-Style-Type" content="text/css">
  <title></title>
  <meta name="Generator" content="Cocoa HTML Writer">
  <meta name="CocoaVersion" content="2685.3">
  <style type="text/css">
    p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Helvetica}
    p.p2 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Helvetica; min-height: 14.0px}
  </style>
</head>
<body>
<p class="p1">from __future__ import annotations</p>
<p class="p2"><br></p>
<p class="p1">import re</p>
<p class="p1">import time</p>
<p class="p1">from dataclasses import dataclass, asdict</p>
<p class="p1">from typing import Optional</p>
<p class="p2"><br></p>
<p class="p1">import requests</p>
<p class="p1">from bs4 import BeautifulSoup</p>
<p class="p1">from flask import Flask, jsonify, render_template_string</p>
<p class="p2"><br></p>
<p class="p1">app = Flask(__name__)</p>
<p class="p2"><br></p>
<p class="p1">HEADERS = {</p>
<p class="p1"><span class="Apple-converted-space">    </span>"User-Agent": (</p>
<p class="p1"><span class="Apple-converted-space">        </span>"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "</p>
<p class="p1"><span class="Apple-converted-space">        </span>"AppleWebKit/537.36 (KHTML, like Gecko) "</p>
<p class="p1"><span class="Apple-converted-space">        </span>"Chrome/125.0.0.0 Safari/537.36"</p>
<p class="p1"><span class="Apple-converted-space">    </span>)</p>
<p class="p1">}</p>
<p class="p1">TIMEOUT = 10</p>
<p class="p1">CACHE_TTL = 180<span class="Apple-converted-space">  </span># seconds</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">@dataclass</p>
<p class="p1">class ParkingLot:</p>
<p class="p1"><span class="Apple-converted-space">    </span>key: str</p>
<p class="p1"><span class="Apple-converted-space">    </span>name: str</p>
<p class="p1"><span class="Apple-converted-space">    </span>address: str</p>
<p class="p1"><span class="Apple-converted-space">    </span>lat: float</p>
<p class="p1"><span class="Apple-converted-space">    </span>lng: float</p>
<p class="p1"><span class="Apple-converted-space">    </span>source_url: str</p>
<p class="p1"><span class="Apple-converted-space">    </span>source_type: str<span class="Apple-converted-space">  </span># 'ipos' | 'times'</p>
<p class="p1"><span class="Apple-converted-space">    </span>status: str = "UNKNOWN"<span class="Apple-converted-space">  </span># EMPTY | FULL | FEW | UNKNOWN</p>
<p class="p1"><span class="Apple-converted-space">    </span>fetched_at: Optional[str] = None</p>
<p class="p1"><span class="Apple-converted-space">    </span>note: Optional[str] = None</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">PARKING_LOTS: list[ParkingLot] = [</p>
<p class="p1"><span class="Apple-converted-space">    </span>ParkingLot(</p>
<p class="p1"><span class="Apple-converted-space">        </span>key="shitadote",</p>
<p class="p1"><span class="Apple-converted-space">        </span>name="したどてスカイパーク",</p>
<p class="p1"><span class="Apple-converted-space">        </span>address="青森県弘前市土手町32",</p>
<p class="p1"><span class="Apple-converted-space">        </span>lat=40.6017,</p>
<p class="p1"><span class="Apple-converted-space">        </span>lng=140.4707,</p>
<p class="p1"><span class="Apple-converted-space">        </span>source_url="https://search.ipos-land.jp/p/detail.aspx?id=K0000089Z",</p>
<p class="p1"><span class="Apple-converted-space">        </span>source_type="ipos",</p>
<p class="p1"><span class="Apple-converted-space">    </span>),</p>
<p class="p1"><span class="Apple-converted-space">    </span>ParkingLot(</p>
<p class="p1"><span class="Apple-converted-space">        </span>key="hirosaki_castle",</p>
<p class="p1"><span class="Apple-converted-space">        </span>name="弘前城公園駐車場",</p>
<p class="p1"><span class="Apple-converted-space">        </span>address="青森県弘前市亀甲町61",</p>
<p class="p1"><span class="Apple-converted-space">        </span>lat=40.6100,</p>
<p class="p1"><span class="Apple-converted-space">        </span>lng=140.4655,</p>
<p class="p1"><span class="Apple-converted-space">        </span>source_url="https://search.ipos-land.jp/p/detail.aspx?id=P0200023Z",</p>
<p class="p1"><span class="Apple-converted-space">        </span>source_type="ipos",</p>
<p class="p1"><span class="Apple-converted-space">    </span>),</p>
<p class="p1"><span class="Apple-converted-space">    </span>ParkingLot(</p>
<p class="p1"><span class="Apple-converted-space">        </span>key="kankokan",</p>
<p class="p1"><span class="Apple-converted-space">        </span>name="タイムズ弘前市立観光館駐車場",</p>
<p class="p1"><span class="Apple-converted-space">        </span>address="青森県弘前市下白銀町2",</p>
<p class="p1"><span class="Apple-converted-space">        </span>lat=40.6077,</p>
<p class="p1"><span class="Apple-converted-space">        </span>lng=140.4653,</p>
<p class="p1"><span class="Apple-converted-space">        </span>source_url="https://times-info.net/P02-aomori/C202/park-detail-BUK0067311/",</p>
<p class="p1"><span class="Apple-converted-space">        </span>source_type="times",</p>
<p class="p1"><span class="Apple-converted-space">    </span>),</p>
<p class="p1"><span class="Apple-converted-space">    </span>ParkingLot(</p>
<p class="p1"><span class="Apple-converted-space">        </span>key="shimodotemachi",</p>
<p class="p1"><span class="Apple-converted-space">        </span>name="タイムズ弘前下土手町",</p>
<p class="p1"><span class="Apple-converted-space">        </span>address="青森県弘前市土手町43",</p>
<p class="p1"><span class="Apple-converted-space">        </span>lat=40.6007,</p>
<p class="p1"><span class="Apple-converted-space">        </span>lng=140.4694,</p>
<p class="p1"><span class="Apple-converted-space">        </span>source_url="https://times-info.net/P02-aomori/C202/park-detail-BUK0037392/",</p>
<p class="p1"><span class="Apple-converted-space">        </span>source_type="times",</p>
<p class="p1"><span class="Apple-converted-space">    </span>),</p>
<p class="p1">]</p>
<p class="p2"><br></p>
<p class="p1">_cache: dict[str, object] = {"ts": 0.0, "data": []}</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">def fetch_html(url: str) -&gt; str:</p>
<p class="p1"><span class="Apple-converted-space">    </span>resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)</p>
<p class="p1"><span class="Apple-converted-space">    </span>resp.raise_for_status()</p>
<p class="p1"><span class="Apple-converted-space">    </span>return resp.text</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">def normalize_text(html: str) -&gt; str:</p>
<p class="p1"><span class="Apple-converted-space">    </span>soup = BeautifulSoup(html, "html.parser")</p>
<p class="p1"><span class="Apple-converted-space">    </span>text = soup.get_text("\n", strip=True)</p>
<p class="p1"><span class="Apple-converted-space">    </span>return re.sub(r"\n+", "\n", text)</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">def detect_status_from_text(text: str) -&gt; tuple[str, Optional[str]]:</p>
<p class="p1"><span class="Apple-converted-space">    </span>t = text.replace("　", " ")</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span># Strongest signals first</p>
<p class="p1"><span class="Apple-converted-space">    </span>if re.search(r"(現在\s*満車|ただいま\s*満車|\b満車\b)", t):</p>
<p class="p1"><span class="Apple-converted-space">        </span>return "FULL", None</p>
<p class="p1"><span class="Apple-converted-space">    </span>if re.search(r"(現在\s*空車|ただいま\s*空車|\b空車\b)", t):</p>
<p class="p1"><span class="Apple-converted-space">        </span>return "EMPTY", None</p>
<p class="p1"><span class="Apple-converted-space">    </span>if re.search(r"(残り\s*わずか|空き\s*わずか|混雑)", t):</p>
<p class="p1"><span class="Apple-converted-space">        </span>return "FEW", None</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span># Sometimes the status label exists but value is omitted or rendered by JS/image.</p>
<p class="p1"><span class="Apple-converted-space">    </span>if "満車/空車等" in t or "満車/空車" in t:</p>
<p class="p1"><span class="Apple-converted-space">        </span>return "UNKNOWN", "満空欄はあるが、文字としては取得できませんでした"</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>return "UNKNOWN", "満空表記を検出できませんでした"</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">def parse_ipos(html: str) -&gt; tuple[str, Optional[str], Optional[str]]:</p>
<p class="p1"><span class="Apple-converted-space">    </span>text = normalize_text(html)</p>
<p class="p1"><span class="Apple-converted-space">    </span>status, note = detect_status_from_text(text)</p>
<p class="p1"><span class="Apple-converted-space">    </span>updated = None</p>
<p class="p1"><span class="Apple-converted-space">    </span>m = re.search(r"(20\d{2}年\d{2}月\s*更新)", text)</p>
<p class="p1"><span class="Apple-converted-space">    </span>if m:</p>
<p class="p1"><span class="Apple-converted-space">        </span>updated = m.group(1)</p>
<p class="p1"><span class="Apple-converted-space">    </span>return status, updated, note</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">def parse_times(html: str) -&gt; tuple[str, Optional[str], Optional[str]]:</p>
<p class="p1"><span class="Apple-converted-space">    </span>text = normalize_text(html)</p>
<p class="p1"><span class="Apple-converted-space">    </span>status, note = detect_status_from_text(text)</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>updated = None</p>
<p class="p1"><span class="Apple-converted-space">    </span>m = re.search(r"(20\d{2}/\d{2}/\d{2}\s+\d{2}:\d{2}\s*現在)", text)</p>
<p class="p1"><span class="Apple-converted-space">    </span>if m:</p>
<p class="p1"><span class="Apple-converted-space">        </span>updated = m.group(1)</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>return status, updated, note</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">def refresh_data() -&gt; list[dict]:</p>
<p class="p1"><span class="Apple-converted-space">    </span>now = time.time()</p>
<p class="p1"><span class="Apple-converted-space">    </span>if now - float(_cache["ts"]) &lt; CACHE_TTL and _cache["data"]:</p>
<p class="p1"><span class="Apple-converted-space">        </span>return _cache["data"]<span class="Apple-converted-space">  </span># type: ignore[return-value]</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>result: list[dict] = []</p>
<p class="p1"><span class="Apple-converted-space">    </span>for lot in PARKING_LOTS:</p>
<p class="p1"><span class="Apple-converted-space">        </span>current = ParkingLot(**asdict(lot))</p>
<p class="p1"><span class="Apple-converted-space">        </span>try:</p>
<p class="p1"><span class="Apple-converted-space">            </span>html = fetch_html(current.source_url)</p>
<p class="p1"><span class="Apple-converted-space">            </span>if current.source_type == "ipos":</p>
<p class="p1"><span class="Apple-converted-space">                </span>current.status, current.fetched_at, current.note = parse_ipos(html)</p>
<p class="p1"><span class="Apple-converted-space">            </span>elif current.source_type == "times":</p>
<p class="p1"><span class="Apple-converted-space">                </span>current.status, current.fetched_at, current.note = parse_times(html)</p>
<p class="p1"><span class="Apple-converted-space">            </span>else:</p>
<p class="p1"><span class="Apple-converted-space">                </span>current.note = "未対応のデータソースです"</p>
<p class="p1"><span class="Apple-converted-space">        </span>except Exception as e:</p>
<p class="p1"><span class="Apple-converted-space">            </span>current.status = "UNKNOWN"</p>
<p class="p1"><span class="Apple-converted-space">            </span>current.note = f"取得失敗: {type(e).__name__}"</p>
<p class="p1"><span class="Apple-converted-space">        </span>result.append(asdict(current))</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>_cache["ts"] = now</p>
<p class="p1"><span class="Apple-converted-space">    </span>_cache["data"] = result</p>
<p class="p1"><span class="Apple-converted-space">    </span>return result</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">@app.get("/api/parking")</p>
<p class="p1">def api_parking():</p>
<p class="p1"><span class="Apple-converted-space">    </span>return jsonify(refresh_data())</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">HTML = """</p>
<p class="p1">&lt;!doctype html&gt;</p>
<p class="p1">&lt;html lang="ja"&gt;</p>
<p class="p1">&lt;head&gt;</p>
<p class="p1"><span class="Apple-converted-space">  </span>&lt;meta charset="utf-8" /&gt;</p>
<p class="p1"><span class="Apple-converted-space">  </span>&lt;meta name="viewport" content="width=device-width, initial-scale=1" /&gt;</p>
<p class="p1"><span class="Apple-converted-space">  </span>&lt;title&gt;弘前さくらまつり 駐車場マップ&lt;/title&gt;</p>
<p class="p1"><span class="Apple-converted-space">  </span>&lt;link</p>
<p class="p1"><span class="Apple-converted-space">    </span>rel="stylesheet"</p>
<p class="p1"><span class="Apple-converted-space">    </span>href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"</p>
<p class="p1"><span class="Apple-converted-space">    </span>integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="</p>
<p class="p1"><span class="Apple-converted-space">    </span>crossorigin=""</p>
<p class="p1"><span class="Apple-converted-space">  </span>/&gt;</p>
<p class="p1"><span class="Apple-converted-space">  </span>&lt;style&gt;</p>
<p class="p1"><span class="Apple-converted-space">    </span>html, body { height: 100%; margin: 0; font-family: system-ui, sans-serif; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>#app { display: grid; grid-template-columns: 340px 1fr; height: 100%; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>#sidebar { padding: 16px; overflow: auto; border-right: 1px solid #ddd; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>#map { height: 100%; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>h1 { font-size: 18px; margin: 0 0 12px; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>.desc { color: #555; font-size: 13px; line-height: 1.5; margin-bottom: 12px; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>.lot { border: 1px solid #e5e5e5; border-radius: 10px; padding: 10px 12px; margin-bottom: 10px; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>.name { font-weight: 700; margin-bottom: 4px; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>.meta { font-size: 12px; color: #666; line-height: 1.4; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>.badge { display: inline-block; padding: 4px 8px; border-radius: 999px; font-size: 12px; font-weight: 700; margin: 6px 0; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>.EMPTY { background: #e7f7ec; color: #176b35; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>.FULL { background: #fdecec; color: #a12727; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>.FEW { background: #fff7e6; color: #a06a00; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>.UNKNOWN { background: #efefef; color: #555; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>.actions a { font-size: 12px; margin-right: 8px; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>.toolbar { display: flex; gap: 8px; margin-bottom: 12px; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>button { padding: 8px 10px; border-radius: 8px; border: 1px solid #ccc; background: white; cursor: pointer; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>@media (max-width: 800px) {</p>
<p class="p1"><span class="Apple-converted-space">      </span>#app { grid-template-columns: 1fr; grid-template-rows: 45% 55%; }</p>
<p class="p1"><span class="Apple-converted-space">      </span>#sidebar { border-right: none; border-bottom: 1px solid #ddd; }</p>
<p class="p1"><span class="Apple-converted-space">    </span>}</p>
<p class="p1"><span class="Apple-converted-space">  </span>&lt;/style&gt;</p>
<p class="p1">&lt;/head&gt;</p>
<p class="p1">&lt;body&gt;</p>
<p class="p1"><span class="Apple-converted-space">  </span>&lt;div id="app"&gt;</p>
<p class="p1"><span class="Apple-converted-space">    </span>&lt;div id="sidebar"&gt;</p>
<p class="p1"><span class="Apple-converted-space">      </span>&lt;h1&gt;弘前さくらまつり 駐車場マップ&lt;/h1&gt;</p>
<p class="p1"><span class="Apple-converted-space">      </span>&lt;div class="desc"&gt;</p>
<p class="p1"><span class="Apple-converted-space">        </span>取れた駐車場だけ満空を表示します。取れないものは「不明」のままにしています。&lt;br&gt;</p>
<p class="p1"><span class="Apple-converted-space">        </span>表示は参考用で、現地表示を優先してください。</p>
<p class="p1"><span class="Apple-converted-space">      </span>&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">      </span>&lt;div class="toolbar"&gt;</p>
<p class="p1"><span class="Apple-converted-space">        </span>&lt;button id="reload"&gt;更新&lt;/button&gt;</p>
<p class="p1"><span class="Apple-converted-space">        </span>&lt;button id="fit"&gt;全体表示&lt;/button&gt;</p>
<p class="p1"><span class="Apple-converted-space">      </span>&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">      </span>&lt;div id="list"&gt;&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">    </span>&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">    </span>&lt;div id="map"&gt;&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">  </span>&lt;/div&gt;</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">  </span>&lt;script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"</p>
<p class="p1"><span class="Apple-converted-space">    </span>integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="</p>
<p class="p1"><span class="Apple-converted-space">    </span>crossorigin=""&gt;&lt;/script&gt;</p>
<p class="p1"><span class="Apple-converted-space">  </span>&lt;script&gt;</p>
<p class="p1"><span class="Apple-converted-space">    </span>const map = L.map('map').setView([40.6065, 140.4685], 14);</p>
<p class="p1"><span class="Apple-converted-space">    </span>L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {</p>
<p class="p1"><span class="Apple-converted-space">      </span>maxZoom: 19,</p>
<p class="p1"><span class="Apple-converted-space">      </span>attribution: '&amp;copy; OpenStreetMap contributors'</p>
<p class="p1"><span class="Apple-converted-space">    </span>}).addTo(map);</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>const markers = new Map();</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>function colorFor(status) {</p>
<p class="p1"><span class="Apple-converted-space">      </span>if (status === 'EMPTY') return '#2e7d32';</p>
<p class="p1"><span class="Apple-converted-space">      </span>if (status === 'FULL') return '#c62828';</p>
<p class="p1"><span class="Apple-converted-space">      </span>if (status === 'FEW') return '#ef6c00';</p>
<p class="p1"><span class="Apple-converted-space">      </span>return '#616161';</p>
<p class="p1"><span class="Apple-converted-space">    </span>}</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>function labelFor(status) {</p>
<p class="p1"><span class="Apple-converted-space">      </span>if (status === 'EMPTY') return '空';</p>
<p class="p1"><span class="Apple-converted-space">      </span>if (status === 'FULL') return '満';</p>
<p class="p1"><span class="Apple-converted-space">      </span>if (status === 'FEW') return '残り少';</p>
<p class="p1"><span class="Apple-converted-space">      </span>return '不明';</p>
<p class="p1"><span class="Apple-converted-space">    </span>}</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>function makeIcon(status) {</p>
<p class="p1"><span class="Apple-converted-space">      </span>const color = colorFor(status);</p>
<p class="p1"><span class="Apple-converted-space">      </span>return L.divIcon({</p>
<p class="p1"><span class="Apple-converted-space">        </span>className: '',</p>
<p class="p1"><span class="Apple-converted-space">        </span>html: `&lt;div style="width:18px;height:18px;border-radius:50%;background:${color};border:2px solid white;box-shadow:0 0 0 1px rgba(0,0,0,.2)"&gt;&lt;/div&gt;`,</p>
<p class="p1"><span class="Apple-converted-space">        </span>iconSize: [18, 18],</p>
<p class="p1"><span class="Apple-converted-space">        </span>iconAnchor: [9, 9]</p>
<p class="p1"><span class="Apple-converted-space">      </span>});</p>
<p class="p1"><span class="Apple-converted-space">    </span>}</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>function popupHtml(lot) {</p>
<p class="p1"><span class="Apple-converted-space">      </span>return `</p>
<p class="p1"><span class="Apple-converted-space">        </span>&lt;div style="min-width:220px"&gt;</p>
<p class="p1"><span class="Apple-converted-space">          </span>&lt;div style="font-weight:700;margin-bottom:6px"&gt;${lot.name}&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">          </span>&lt;div style="margin-bottom:6px"&gt;状態: &lt;b&gt;${labelFor(lot.status)}&lt;/b&gt;&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">          </span>&lt;div style="font-size:12px;color:#555;line-height:1.5"&gt;</p>
<p class="p1"><span class="Apple-converted-space">            </span>${lot.address}&lt;br&gt;</p>
<p class="p1"><span class="Apple-converted-space">            </span>更新元: &lt;a href="${lot.source_url}" target="_blank" rel="noopener noreferrer"&gt;確認ページ&lt;/a&gt;&lt;br&gt;</p>
<p class="p1"><span class="Apple-converted-space">            </span>${lot.fetched_at ? `ページ表示: ${lot.fetched_at}&lt;br&gt;` : ''}</p>
<p class="p1"><span class="Apple-converted-space">            </span>${lot.note ? `補足: ${lot.note}` : ''}</p>
<p class="p1"><span class="Apple-converted-space">          </span>&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">        </span>&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">      </span>`;</p>
<p class="p1"><span class="Apple-converted-space">    </span>}</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>function listHtml(lot) {</p>
<p class="p1"><span class="Apple-converted-space">      </span>const q = encodeURIComponent(`${lot.name} ${lot.address}`);</p>
<p class="p1"><span class="Apple-converted-space">      </span>return `</p>
<p class="p1"><span class="Apple-converted-space">        </span>&lt;div class="lot"&gt;</p>
<p class="p1"><span class="Apple-converted-space">          </span>&lt;div class="name"&gt;${lot.name}&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">          </span>&lt;div&gt;&lt;span class="badge ${lot.status}"&gt;${labelFor(lot.status)}&lt;/span&gt;&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">          </span>&lt;div class="meta"&gt;</p>
<p class="p1"><span class="Apple-converted-space">            </span>${lot.address}&lt;br&gt;</p>
<p class="p1"><span class="Apple-converted-space">            </span>${lot.fetched_at ? `ページ表示: ${lot.fetched_at}&lt;br&gt;` : ''}</p>
<p class="p1"><span class="Apple-converted-space">            </span>${lot.note ? `補足: ${lot.note}&lt;br&gt;` : ''}</p>
<p class="p1"><span class="Apple-converted-space">          </span>&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">          </span>&lt;div class="actions" style="margin-top:6px"&gt;</p>
<p class="p1"><span class="Apple-converted-space">            </span>&lt;a href="${lot.source_url}" target="_blank" rel="noopener noreferrer"&gt;満空ページ&lt;/a&gt;</p>
<p class="p1"><span class="Apple-converted-space">            </span>&lt;a href="https://www.google.com/maps/search/?api=1&amp;query=${q}" target="_blank" rel="noopener noreferrer"&gt;Googleマップ&lt;/a&gt;</p>
<p class="p1"><span class="Apple-converted-space">          </span>&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">        </span>&lt;/div&gt;</p>
<p class="p1"><span class="Apple-converted-space">      </span>`;</p>
<p class="p1"><span class="Apple-converted-space">    </span>}</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>async function loadData() {</p>
<p class="p1"><span class="Apple-converted-space">      </span>const res = await fetch('/api/parking');</p>
<p class="p1"><span class="Apple-converted-space">      </span>const lots = await res.json();</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">      </span>document.getElementById('list').innerHTML = lots.map(listHtml).join('');</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">      </span>const bounds = [];</p>
<p class="p1"><span class="Apple-converted-space">      </span>for (const lot of lots) {</p>
<p class="p1"><span class="Apple-converted-space">        </span>bounds.push([lot.lat, lot.lng]);</p>
<p class="p1"><span class="Apple-converted-space">        </span>const existing = markers.get(lot.key);</p>
<p class="p1"><span class="Apple-converted-space">        </span>if (existing) {</p>
<p class="p1"><span class="Apple-converted-space">          </span>existing.setIcon(makeIcon(lot.status));</p>
<p class="p1"><span class="Apple-converted-space">          </span>existing.setPopupContent(popupHtml(lot));</p>
<p class="p1"><span class="Apple-converted-space">        </span>} else {</p>
<p class="p1"><span class="Apple-converted-space">          </span>const marker = L.marker([lot.lat, lot.lng], { icon: makeIcon(lot.status) })</p>
<p class="p1"><span class="Apple-converted-space">            </span>.addTo(map)</p>
<p class="p1"><span class="Apple-converted-space">            </span>.bindPopup(popupHtml(lot));</p>
<p class="p1"><span class="Apple-converted-space">          </span>markers.set(lot.key, marker);</p>
<p class="p1"><span class="Apple-converted-space">        </span>}</p>
<p class="p1"><span class="Apple-converted-space">      </span>}</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">      </span>if (bounds.length) {</p>
<p class="p1"><span class="Apple-converted-space">        </span>map.fitBounds(bounds, { padding: [24, 24] });</p>
<p class="p1"><span class="Apple-converted-space">      </span>}</p>
<p class="p1"><span class="Apple-converted-space">    </span>}</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>document.getElementById('reload').addEventListener('click', loadData);</p>
<p class="p1"><span class="Apple-converted-space">    </span>document.getElementById('fit').addEventListener('click', () =&gt; {</p>
<p class="p1"><span class="Apple-converted-space">      </span>const pts = [...markers.values()].map(m =&gt; m.getLatLng());</p>
<p class="p1"><span class="Apple-converted-space">      </span>if (pts.length) map.fitBounds(L.latLngBounds(pts), { padding: [24, 24] });</p>
<p class="p1"><span class="Apple-converted-space">    </span>});</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>loadData();</p>
<p class="p1"><span class="Apple-converted-space">    </span>setInterval(loadData, 180000);</p>
<p class="p1"><span class="Apple-converted-space">  </span>&lt;/script&gt;</p>
<p class="p1">&lt;/body&gt;</p>
<p class="p1">&lt;/html&gt;</p>
<p class="p1">"""</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">@app.get("/")</p>
<p class="p1">def index():</p>
<p class="p1"><span class="Apple-converted-space">    </span>return render_template_string(HTML)</p>
<p class="p2"><br></p>
<p class="p2"><br></p>
<p class="p1">if __name__ == "__main__":</p>
<p class="p1"><span class="Apple-converted-space">    </span>app.run(debug=True, port=8000)</p>
</body>
</html>
