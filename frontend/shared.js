const API_BASE = 'http://localhost:8000/api';
let authToken = localStorage.getItem('irctc_token') || null;
let authUser = JSON.parse(localStorage.getItem('irctc_user') || 'null');

const TRAINS = [
  {number:'12301',name:'Howrah Rajdhani Express',type:'RAJ',typeLabel:'Rajdhani',dep:'16:35',arr:'10:05',dur:'17h 30m',days:['M','T','W','Th','F','S','Su'],pantry:true,avail:[{cls:'1A',label:'First AC',seats:'3 Avail',fare:4800,type:'avail'},{cls:'2A',label:'Second AC',seats:'12 Avail',fare:2900,type:'avail'},{cls:'3A',label:'Third AC',seats:'WL/4',fare:2050,type:'wl'}]},
  {number:'12951',name:'Mumbai Rajdhani Express',type:'RAJ',typeLabel:'Rajdhani',dep:'17:40',arr:'08:35',dur:'14h 55m',days:['M','W','F','Su'],pantry:true,avail:[{cls:'2A',label:'Second AC',seats:'5 Avail',fare:2900,type:'avail'},{cls:'3A',label:'Third AC',seats:'18 Avail',fare:2050,type:'avail'},{cls:'1A',label:'First AC',seats:'NA',fare:4800,type:'na'}]},
  {number:'22209',name:'Mumbai Duronto Express',type:'DUR',typeLabel:'Duronto',dep:'23:10',arr:'15:55',dur:'16h 45m',days:['T','Th','S'],pantry:false,avail:[{cls:'1A',label:'First AC',seats:'7 Avail',fare:4200,type:'avail'},{cls:'2A',label:'Second AC',seats:'22 Avail',fare:2500,type:'avail'},{cls:'3A',label:'Third AC',seats:'31 Avail',fare:1800,type:'avail'},{cls:'SL',label:'Sleeper',seats:'WL/8',fare:620,type:'wl'}]},
  {number:'12137',name:'Punjab Mail',type:'MAIL',typeLabel:'Mail',dep:'19:05',arr:'14:30',dur:'19h 25m',days:['M','T','W','Th','F','S','Su'],pantry:false,avail:[{cls:'2A',label:'Second AC',seats:'1 Avail',fare:2200,type:'avail'},{cls:'3A',label:'Third AC',seats:'WL/3',fare:1600,type:'wl'},{cls:'SL',label:'Sleeper',seats:'62 Avail',fare:520,type:'avail'},{cls:'GN',label:'General',seats:'Avail',fare:200,type:'avail'}]},
  {number:'19019',name:'Dehradun Express',type:'EXP',typeLabel:'Express',dep:'22:25',arr:'20:10',dur:'21h 45m',days:['M','T','W','Th','F','S','Su'],pantry:false,avail:[{cls:'3A',label:'Third AC',seats:'9 Avail',fare:1750,type:'avail'},{cls:'SL',label:'Sleeper',seats:'78 Avail',fare:580,type:'avail'},{cls:'GN',label:'General',seats:'Avail',fare:200,type:'avail'}]},
  {number:'12009',name:'Mumbai Shatabdi Express',type:'SHT',typeLabel:'Shatabdi',dep:'06:25',arr:'08:30',dur:'2h 05m',days:['M','T','W','Th','F','S'],pantry:true,avail:[{cls:'CC',label:'Chair Car',seats:'24 Avail',fare:485,type:'avail'},{cls:'EC',label:'Exec Chair Car',seats:'6 Avail',fare:975,type:'avail'}]},
];

function navbar(activePage) {
  var userHtml = authUser
    ? '<a class="nav-link active" href="mybookings.html">&#128100; ' + (authUser.first_name || authUser.username) + '</a><a class="nav-link" href="#" onclick="doLogout();return false;">Logout</a>'
    : '<a class="nav-link btn-orange" href="#" onclick="showLoginModal();return false;">Login / Register</a>';
  return '<div class="promo">&#127881; Special Offer: 10% cashback on Tatkal bookings via IRCTC Wallet &mdash; Limited period!</div>'
    + '<nav class="navbar">'
    + '<div class="logo" onclick="window.location=\'index.html\'">'
    + '<span>IRCTC</span><span class="logo-badge">Rail</span>'
    + '</div>'
    + '<div class="nav-links">'
    + '<a class="nav-link' + (activePage === 'home' ? ' active' : '') + '" href="index.html">Home</a>'
    + '<a class="nav-link' + (activePage === 'trains' ? ' active' : '') + '" href="trains.html">Trains</a>'
    + '<a class="nav-link' + (activePage === 'pnr' ? ' active' : '') + '" href="pnr.html">PNR Status</a>'
    + '<a class="nav-link' + (activePage === 'services' ? ' active' : '') + '" href="services.html">Services</a>'
    + '<a class="nav-link' + (activePage === 'about' ? ' active' : '') + '" href="about.html">About</a>'
    + '<a class="nav-link' + (activePage === 'contact' ? ' active' : '') + '" href="contact.html">Contact</a>'
    + userHtml
    + '</div>'
    + '</nav>';
}

function footer() {
  return '<footer class="footer">'
    + '<div class="footer-grid">'
    + '<div class="footer-brand">'
    + '<div class="logo"><span>IRCTC</span><span class="logo-badge">Rail</span></div>'
    + '<p>Indian Railway Catering and Tourism Corporation Ltd. &mdash; The official ticketing arm of Indian Railways. Serving millions of passengers daily across 7,000+ stations.</p>'
    + '</div>'
    + '<div class="footer-col"><h4>Quick Links</h4>'
    + '<a href="index.html">Book Ticket</a><a href="pnr.html">PNR Status</a>'
    + '<a href="trains.html">Train Search</a><a href="mybookings.html">My Bookings</a>'
    + '<a href="services.html">All Services</a>'
    + '</div>'
    + '<div class="footer-col"><h4>Services</h4>'
    + '<a href="services.html">e-Catering</a><a href="services.html">Platform Info</a>'
    + '<a href="services.html">Train Alert</a><a href="services.html">Season Pass</a>'
    + '<a href="services.html">Tourism</a>'
    + '</div>'
    + '<div class="footer-col"><h4>Company</h4>'
    + '<a href="about.html">About IRCTC</a><a href="contact.html">Contact Us</a>'
    + '<a href="about.html">Careers</a><a href="about.html">Press</a>'
    + '</div>'
    + '</div>'
    + '<div class="footer-bottom">'
    + '<span>&copy; 2024 IRCTC Ltd. | Ministry of Railways, Govt. of India</span>'
    + '<span><a href="#" style="color:rgba(255,255,255,.5);margin:0 8px">Privacy Policy</a>'
    + '<a href="#" style="color:rgba(255,255,255,.5);margin:0 8px">Terms</a>'
    + '<a href="#" style="color:rgba(255,255,255,.5);margin:0 8px">Refund Policy</a></span>'
    + '</div>'
    + '</footer>';
}

function loginModal() {
  return '<div id="login-modal" class="mbdrop hidden" onclick="if(event.target===this)this.classList.add(\'hidden\')">'
    + '<div class="modal" style="max-width:420px">'
    + '<div class="mhead"><span>&#128272;</span><h3 id="auth-modal-title">Login to IRCTC</h3>'
    + '<button class="mclose" onclick="document.getElementById(\'login-modal\').classList.add(\'hidden\')">&#x2715;</button></div>'
    + '<div style="padding:1.5rem">'
    + '<div id="lf">'
    + '<div class="fgrp" style="margin-bottom:12px"><label>Username / Email</label><input id="l-user" type="text" placeholder="Enter username or email"></div>'
    + '<div class="fgrp" style="margin-bottom:6px"><label>Password</label><input id="l-pass" type="password" placeholder="Enter password"></div>'
    + '<div style="text-align:right;margin-bottom:14px"><a href="#" style="font-size:12px;color:var(--blue)">Forgot Password?</a></div>'
    + '<button class="btn-blue-full" style="margin-top:0" onclick="doLogin()">Login</button>'
    + '<div style="text-align:center;margin-top:12px;font-size:13px;color:var(--muted)">New user? <span onclick="document.getElementById(\'lf\').classList.add(\'hidden\');document.getElementById(\'rf\').classList.remove(\'hidden\')" style="color:var(--blue);cursor:pointer;font-weight:700">Register &#8594;</span></div>'
    + '</div>'
    + '<div id="rf" class="hidden">'
    + '<div class="frow"><div class="fgrp"><label>First Name</label><input id="r-fn" type="text" placeholder="Rahul"></div><div class="fgrp"><label>Last Name</label><input id="r-ln" type="text" placeholder="Sharma"></div></div>'
    + '<div class="fgrp" style="margin-bottom:10px"><label>Username</label><input id="r-un" type="text" placeholder="rahul99"></div>'
    + '<div class="fgrp" style="margin-bottom:10px"><label>Email</label><input id="r-em" type="email" placeholder="rahul@example.com"></div>'
    + '<div class="fgrp" style="margin-bottom:10px"><label>Mobile</label><input id="r-ph" type="tel" placeholder="9876543210"></div>'
    + '<div class="frow" style="margin-bottom:14px"><div class="fgrp"><label>Password</label><input id="r-pw" type="password" placeholder="Min 8 chars"></div><div class="fgrp"><label>Confirm</label><input id="r-pw2" type="password" placeholder="Repeat"></div></div>'
    + '<button class="btn-blue-full" style="margin-top:0" onclick="doRegister()">Create Account</button>'
    + '<div style="text-align:center;margin-top:10px;font-size:13px;color:var(--muted)">Have account? <span onclick="document.getElementById(\'rf\').classList.add(\'hidden\');document.getElementById(\'lf\').classList.remove(\'hidden\')" style="color:var(--blue);cursor:pointer;font-weight:700">Login &#8594;</span></div>'
    + '</div>'
    + '</div>'
    + '</div>'
    + '</div>';
}

function showLoginModal() {
  document.getElementById('login-modal').classList.remove('hidden');
}

async function doLogin() {
  var u = document.getElementById('l-user').value;
  var p = document.getElementById('l-pass').value;
  try {
    var r = await fetch(API_BASE + '/auth/login/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({username:u, password:p})});
    var d = await r.json();
    if (r.ok) {
      authToken = d.access;
      localStorage.setItem('irctc_token', d.access);
      if (d.user) { authUser = d.user; localStorage.setItem('irctc_user', JSON.stringify(d.user)); }
      location.reload();
    } else {
      alert(d.detail || 'Invalid credentials');
    }
  } catch(e) {
    alert('Demo mode: Backend not connected.\nFor a real deployment, connect your Django API.');
  }
}

async function doRegister() {
  var body = {
    username: document.getElementById('r-un').value,
    email: document.getElementById('r-em').value,
    password: document.getElementById('r-pw').value,
    password2: document.getElementById('r-pw2').value,
    first_name: document.getElementById('r-fn').value,
    last_name: document.getElementById('r-ln').value,
    phone: document.getElementById('r-ph').value
  };
  try {
    var r = await fetch(API_BASE + '/auth/register/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
    var d = await r.json();
    if (r.ok) {
      authToken = d.tokens.access;
      localStorage.setItem('irctc_token', d.tokens.access);
      localStorage.setItem('irctc_user', JSON.stringify(d.user));
      location.reload();
    } else {
      alert(Object.values(d).flat().join('\n'));
    }
  } catch(e) {
    alert('Registration successful (demo mode)!');
    document.getElementById('login-modal').classList.add('hidden');
  }
}

function doLogout() {
  localStorage.removeItem('irctc_token');
  localStorage.removeItem('irctc_user');
  authToken = null; authUser = null;
  location.reload();
}

var currentTrain = null, paxCount = 1, currentFare = 0, currentCls = '';

function bookingModal() {
  return '<div id="booking-modal" class="mbdrop hidden" onclick="if(event.target===this)this.classList.add(\'hidden\')">'
    + '<div class="modal"><div class="mhead"><span>&#127915;</span><h3 id="bm-title">Book Ticket</h3>'
    + '<button class="mclose" onclick="document.getElementById(\'booking-modal\').classList.add(\'hidden\')">&#x2715;</button></div>'
    + '<div id="bm-form" class="mbody">'
    + '<div style="background:var(--light);border-radius:8px;padding:12px 14px;margin-bottom:16px;font-size:13px">'
    + '<div style="display:flex;justify-content:space-between;align-items:center;font-weight:700"><span id="bm-route">-</span><span class="badge blue" id="bm-cls">3A</span></div>'
    + '<div style="color:var(--muted);margin-top:4px;font-size:12px" id="bm-date">-</div></div>'
    + '<div id="pax-container"></div>'
    + '<button onclick="addPax()" style="background:none;border:1.5px dashed var(--blue);color:var(--blue);padding:9px;border-radius:8px;width:100%;cursor:pointer;font-size:13px;font-weight:600;font-family:Noto Sans,sans-serif;margin-top:4px">+ Add Passenger (Max 6)</button>'
    + '<div style="margin-top:14px"><div style="font-size:11px;font-weight:700;color:var(--muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:.5px">Contact Details</div>'
    + '<div class="frow"><div class="fgrp"><label>Mobile</label><input type="tel" id="bm-mobile" placeholder="10-digit number"></div>'
    + '<div class="fgrp"><label>Email</label><input type="email" id="bm-email" placeholder="your@email.com"></div></div></div>'
    + '<div class="fare-box"><div style="font-size:13px;font-weight:700;color:var(--dark);margin-bottom:10px">Fare Summary</div>'
    + '<div class="fare-row"><span>Base Fare (<span id="bm-pcount">1</span> pax)</span><span id="bm-base">&#8377;0</span></div>'
    + '<div class="fare-row"><span>Reservation Charges</span><span id="bm-res">&#8377;40</span></div>'
    + '<div class="fare-row"><span>IRCTC Service Fee</span><span>&#8377;15</span></div>'
    + '<div class="fare-row"><span>GST (5%)</span><span id="bm-gst">&#8377;0</span></div>'
    + '<div class="fare-row total"><span>Total Payable</span><span id="bm-total">&#8377;0</span></div></div>'
    + '<button class="btn-orange-full" onclick="showPayment()">Proceed to Payment &#8594;</button></div>'
    + '<div id="bm-payment" class="mbody hidden">'
    + '<div style="font-size:15px;font-weight:700;margin-bottom:14px">Select Payment Method</div>'
    + '<label style="display:flex;align-items:center;gap:12px;border:1.5px solid var(--border);border-radius:10px;padding:14px;cursor:pointer;margin-bottom:8px"><input type="radio" name="pm" checked> <span style="font-size:14px;font-weight:500">&#128179; UPI &mdash; PhonePe, Google Pay, Paytm</span></label>'
    + '<label style="display:flex;align-items:center;gap:12px;border:1.5px solid var(--border);border-radius:10px;padding:14px;cursor:pointer;margin-bottom:8px"><input type="radio" name="pm"> <span style="font-size:14px;font-weight:500">&#127968; Net Banking &mdash; All major banks</span></label>'
    + '<label style="display:flex;align-items:center;gap:12px;border:1.5px solid var(--border);border-radius:10px;padding:14px;cursor:pointer;margin-bottom:8px"><input type="radio" name="pm"> <span style="font-size:14px;font-weight:500">&#128179; Debit / Credit Card</span></label>'
    + '<label style="display:flex;align-items:center;gap:12px;border:1.5px solid var(--border);border-radius:10px;padding:14px;cursor:pointer;margin-bottom:8px"><input type="radio" name="pm"> <span style="font-size:14px;font-weight:500">&#128091; IRCTC Wallet</span></label>'
    + '<div style="background:#fffbeb;border-radius:8px;padding:10px 14px;margin-top:4px;font-size:12px;color:#92400e;border:1px solid #fde68a">&#9888; Seats held for <strong>15 minutes</strong>. Complete payment to confirm.</div>'
    + '<button class="btn-orange-full" onclick="confirmBooking()">Pay &#8377;<span id="bm-pay">0</span> &amp; Confirm</button>'
    + '<button onclick="document.getElementById(\'bm-form\').classList.remove(\'hidden\');document.getElementById(\'bm-payment\').classList.add(\'hidden\')" style="width:100%;background:none;border:none;color:var(--muted);font-size:13px;cursor:pointer;padding:8px;margin-top:4px">&#8592; Back</button>'
    + '</div>'
    + '<div id="bm-success" class="hidden"><div style="text-align:center;padding:2.5rem 1.5rem">'
    + '<div style="font-size:64px;margin-bottom:14px">&#127881;</div>'
    + '<div style="font-family:Rajdhani,sans-serif;font-size:24px;font-weight:700;color:var(--green)">Booking Confirmed!</div>'
    + '<div style="color:var(--muted);font-size:13px;margin-top:6px">Your PNR Number</div>'
    + '<div id="bm-pnr" style="font-family:Rajdhani,sans-serif;font-size:30px;font-weight:700;color:var(--blue);letter-spacing:4px;background:var(--light);padding:10px 24px;border-radius:8px;display:inline-block;margin:10px 0"></div>'
    + '<div style="background:#fff;border:2px dashed var(--border);border-radius:10px;padding:16px;text-align:left;margin-top:10px;font-size:13px">'
    + '<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #f1f5f9"><span style="color:var(--muted)">Train</span><span id="bm-ctrain" style="font-weight:700"></span></div>'
    + '<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #f1f5f9"><span style="color:var(--muted)">Route</span><span id="bm-croute" style="font-weight:700"></span></div>'
    + '<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #f1f5f9"><span style="color:var(--muted)">Date</span><span id="bm-cdate" style="font-weight:700"></span></div>'
    + '<div style="display:flex;justify-content:space-between;padding:5px 0"><span style="color:var(--muted)">Status</span><span style="font-weight:700;color:var(--green)">&#10003; CONFIRMED</span></div>'
    + '</div>'
    + '<div style="display:flex;gap:8px;margin-top:16px">'
    + '<button onclick="document.getElementById(\'booking-modal\').classList.add(\'hidden\')" style="flex:1;background:#f1f5f9;border:none;padding:12px;border-radius:8px;cursor:pointer;font-weight:600;font-size:14px">Close</button>'
    + '<button style="flex:1;background:var(--blue);color:#fff;border:none;padding:12px;border-radius:8px;cursor:pointer;font-weight:600;font-size:14px">&#128229; Download Ticket</button>'
    + '</div></div></div></div></div>';
}

function paxTemplate(n) {
  return '<div class="pax-box" style="' + (n > 1 ? 'margin-top:10px' : '') + '">'
    + '<div style="font-size:13px;font-weight:700;color:var(--dark);margin-bottom:10px;display:flex;justify-content:space-between">Passenger Details <span style="color:var(--muted);font-size:12px">Pax ' + n + '</span></div>'
    + '<div class="frow"><div class="fgrp"><label>Full Name</label><input type="text" placeholder="As on ID card"></div><div class="fgrp"><label>Age</label><input type="number" min="1" max="120" placeholder="Age"></div></div>'
    + '<div class="frow"><div class="fgrp"><label>Gender</label><select><option>Male</option><option>Female</option><option>Other</option></select></div>'
    + '<div class="fgrp"><label>Berth Preference</label><select><option value="NP">No Preference</option><option value="LB">Lower</option><option value="MB">Middle</option><option value="UB">Upper</option><option value="SL">Side Lower</option><option value="SU">Side Upper</option></select></div></div>'
    + '</div>';
}

function openBooking(trainData, cls, label, fare, src, dst, dt) {
  currentTrain = (typeof trainData === 'string') ? JSON.parse(trainData) : trainData;
  currentFare = fare; currentCls = cls; paxCount = 1;
  document.getElementById('bm-title').textContent = currentTrain.number + ' \u00b7 ' + currentTrain.name;
  document.getElementById('bm-route').textContent = src + ' \u2192 ' + dst;
  document.getElementById('bm-cls').textContent = cls + ' \u2014 ' + label;
  document.getElementById('bm-date').textContent = dt || '';
  document.getElementById('pax-container').innerHTML = paxTemplate(1);
  updateFare();
  document.getElementById('bm-form').classList.remove('hidden');
  document.getElementById('bm-payment').classList.add('hidden');
  document.getElementById('bm-success').classList.add('hidden');
  document.getElementById('booking-modal').classList.remove('hidden');
}

function addPax() {
  if (paxCount >= 6) { alert('Maximum 6 passengers per booking'); return; }
  paxCount++;
  document.getElementById('pax-container').insertAdjacentHTML('beforeend', paxTemplate(paxCount));
  updateFare();
}

function updateFare() {
  var base = currentFare * paxCount;
  var res = 40 * paxCount, svc = 15, gst = Math.round(base * 0.05);
  var total = base + res + svc + gst;
  document.getElementById('bm-pcount').textContent = paxCount;
  document.getElementById('bm-base').textContent = '\u20b9' + base;
  document.getElementById('bm-res').textContent = '\u20b9' + res;
  document.getElementById('bm-gst').textContent = '\u20b9' + gst;
  document.getElementById('bm-total').textContent = '\u20b9' + total;
  document.getElementById('bm-pay').textContent = total;
}

function showPayment() {
  document.getElementById('bm-form').classList.add('hidden');
  document.getElementById('bm-payment').classList.remove('hidden');
}

function confirmBooking() {
  var pnr = Math.floor(1000000000 + Math.random() * 9000000000).toString();
  document.getElementById('bm-pnr').textContent = pnr;
  document.getElementById('bm-ctrain').textContent = currentTrain ? currentTrain.number + ' ' + currentTrain.name : '-';
  document.getElementById('bm-croute').textContent = document.getElementById('bm-route').textContent;
  document.getElementById('bm-cdate').textContent = document.getElementById('bm-date').textContent;
  document.getElementById('bm-payment').classList.add('hidden');
  document.getElementById('bm-success').classList.remove('hidden');
}

function searchForm(selectedSrc, selectedDst) {
  selectedSrc = selectedSrc || '';
  selectedDst = selectedDst || '';
  var tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  var ds = tomorrow.toISOString().split('T')[0];
  return '<div class="search-card">'
    + '<div class="trip-type">'
    + '<label class="rlabel"><input type="radio" name="tt" checked> Book Tickets</label>'
    + '<label class="rlabel"><input type="radio" name="tt"> Check Availability</label>'
    + '<label class="rlabel"><input type="radio" name="tt"> Tatkal</label>'
    + '<label class="rlabel"><input type="radio" name="tt"> Season Pass</label>'
    + '</div>'
    + '<div class="srow">'
    + '<div class="igrp"><label>From Station</label><input type="text" id="src" list="stlist" value="' + (selectedSrc || 'Mumbai CST (CSTM)') + '" placeholder="City / Station Code"></div>'
    + '<button class="swap-btn" onclick="var s=document.getElementById(\'src\'),d=document.getElementById(\'dst\');var t=s.value;s.value=d.value;d.value=t;">&#8644;</button>'
    + '<div class="igrp"><label>To Station</label><input type="text" id="dst" list="stlist" value="' + (selectedDst || 'New Delhi (NDLS)') + '" placeholder="City / Station Code"></div>'
    + '<div class="igrp"><label>Date of Journey</label><input type="date" id="jdate" value="' + ds + '"></div>'
    + '<button class="sbtn" onclick="doSearch()">&#128269; Search Trains</button>'
    + '</div>'
    + '<datalist id="stlist"><option value="Mumbai CST (CSTM)"><option value="New Delhi (NDLS)"><option value="Howrah Junction (HWH)">'
    + '<option value="Chennai Central (MAS)"><option value="KSR Bengaluru City (SBC)"><option value="Secunderabad Junction (SC)">'
    + '<option value="Ahmedabad Junction (ADI)"><option value="Pune Junction (PUNE)"><option value="Jaipur Junction (JP)">'
    + '<option value="Lucknow Charbagh (LKO)"><option value="Bhopal Junction (BPL)"><option value="Nagpur Junction (NGP)">'
    + '</datalist>'
    + '<div class="class-row">'
    + '<span style="font-size:12px;font-weight:700;color:var(--muted)">Class:</span>'
    + '<span class="cchip sel" onclick="selCls(this,\'\')">All</span>'
    + '<span class="cchip" onclick="selCls(this,\'SL\')">Sleeper</span>'
    + '<span class="cchip" onclick="selCls(this,\'3A\')">Third AC</span>'
    + '<span class="cchip" onclick="selCls(this,\'2A\')">Second AC</span>'
    + '<span class="cchip" onclick="selCls(this,\'1A\')">First AC</span>'
    + '<span class="cchip" onclick="selCls(this,\'CC\')">Chair Car</span>'
    + '</div></div>';
}

function selCls(el, v) {
  document.querySelectorAll('.cchip').forEach(function(c) { c.classList.remove('sel'); });
  el.classList.add('sel');
}

function renderTrainCard(t, src, dst, dt) {
  var allDays = ['M','T','W','Th','F','S','Su'];
  var srcMatch = src.match(/\(([^)]+)\)/);
  var dstMatch = dst.match(/\(([^)]+)\)/);
  var srcCode = srcMatch ? srcMatch[1] : src.slice(0,4).toUpperCase();
  var dstCode = dstMatch ? dstMatch[1] : dst.slice(0,4).toUpperCase();
  var srcName = src.split('(')[0].trim();
  var dstName = dst.split('(')[0].trim();
  var tJson = JSON.stringify(t).replace(/\\/g,'\\\\').replace(/'/g,"\\'");

  var availHtml = t.avail.map(function(a) {
    return '<div class="achip ' + a.type + '" onclick="openBooking(\'' + tJson + '\',\'' + a.cls + '\',\'' + a.label + '\',' + a.fare + ',\'' + srcName + '\',\'' + dstName + '\',\'' + dt + '\')">'
      + '<div class="acls">' + a.cls + '</div>'
      + '<div class="aseats">' + a.seats + '</div>'
      + '<div class="afare">&#8377;' + a.fare + '</div>'
      + '</div>';
  }).join('');

  var daysHtml = allDays.map(function(d) {
    return '<span class="dbadge ' + (t.days.indexOf(d) !== -1 ? 'runs' : 'no') + '">' + d + '</span>';
  }).join('');

  return '<div class="train-card fade-up">'
    + '<div class="tc-head">'
    + '<span class="tn">' + t.number + '</span>'
    + '<span class="tname">' + t.name + '</span>'
    + (t.pantry ? '<span class="pantry-tag">&#127869; Pantry</span>' : '')
    + '<span class="ttype">' + t.typeLabel + '</span>'
    + '</div>'
    + '<div class="tc-body">'
    + '<div><div class="ttime">' + t.dep + '</div><div class="tcode">' + srcCode + '</div><div class="tfull">' + srcName + '</div></div>'
    + '<div class="tdur"><div class="tdur-text">' + t.dur + '</div>'
    + '<div class="tdur-line"><div class="tdot"></div><div class="tline"></div><div class="tdot"></div></div>'
    + '<div style="font-size:11px;color:var(--muted)">' + dt + '</div></div>'
    + '<div style="text-align:right"><div class="ttime">' + t.arr + '</div><div class="tcode">' + dstCode + '</div><div class="tfull">' + dstName + '</div></div>'
    + '</div>'
    + '<div class="avail-grid">' + availHtml + '</div>'
    + '<div class="days-row">' + daysHtml + '</div>'
    + '</div>';
}
