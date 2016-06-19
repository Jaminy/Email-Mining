*/

Components.utils.import("resource://gre/modules/Services.jsm");


var objTelify = {

digits_min: 7,
digits_max: 16,

hilite_color: new Array(0,0,255),
hilite_bgcolor: new Array(255,255,0),

// special chars
sc_nbsp: String.fromCharCode(0xa0),

// chars which look like dashes
token_dash:
        String.fromCharCode(0x2013) +
        String.fromCharCode(0x2014) +
        String.fromCharCode(0x2212),

exclPatternList: [
        /^\d{2}\.\d{2} *(-|–) *\d{2}\.\d{2}$/,  // time range e.g. 08.00 - 17.00
        /^\d{2}\/\d{2}\/\d{2}$/,        // date e.g. 09/03/09
        /^\d{2}\/\d{2} *(-|–) *\d{2}\/\d{2}$/,  // date range e.g. 01/05 - 05/06
        /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/, // ip address
        /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} *\/ *(8|16|24)$/,  // ip address with subn
et
        /^[0-3]?[0-9][\/\.-][0-3]?[0-9][\/\.-](19|20)\d{2} *(-|–) *\d{2}\.\d{2}$/,
et
        /^[0-3]?[0-9][\/\.-][0-3]?[0-9][\/\.-](19|20)\d{2} *(-|–) *\d{2}\.\d{2}$/,
      // date and time e.g. 09.03.2009 - 17.59
        /^\d{2}[\.\:]\d{2} +[0-3]?[0-9][\/\.-][0-3]?[0-9][\/\.-](19|20)?\d{2}$/,
        // date and time e.g. 17:59 09/03/2009
        /^[0-3]?[0-9][\/\.-] *[0-3]?[0-9][\/\.-] *(19|20)\d{2}$/,       // date e.g. 09/03/2009, 09.03.2009, 09-03-2009
        /^[0-3]?[0-9]\.?[\/-][0-3]?[0-9]\. *[0-1]?[0-9]\. *(19|20)\d{2}$/,      // two days e.g. 20/21.5.2010
        /^[0-3]?[0-9][\/\.-][0-3]?[0-9]\.? *(-|–) *[0-3]?[0-9][\/\.-][0-3]?[0-9]\.?$/,
  // date range days
        /^[0-3]?[0-9][\/\.-][0-3]?[0-9][\/\.-]? *(-|–) *[0-3]?[0-9][\/\.-][0-3]?[0-9][\/\.-]\d{2}$/,    // date range short
        /^[0-3]?[0-9][\/\.-][0-3]?[0-9][\/\.-]\d{2} *(-|–) *[0-3]?[0-9][\/\.-][0-3]?[0-9][\/\.-]\d{2}$/,        // date range short
        /^[0-3]?[0-9][\/\.-][0-3]?[0-9][\/\.-] *(-|–) *[0-3]?[0-9][\/\.-][0-3]?[0-9][\/\.-](19|20)\d{2}$/,      // date range medium
        /^([0-3]?[0-9][\/\.-])?[0-3]?[0-9][\/\.-](19|20)\d{2} *(-|–) *([0-3]?[0-9][\/\.-])?[0-3]?[0-9][\/\.-](19|20)\d{2}$/,    // date range long
        /^[0-9]([ \.\,]000)+$/, // just a big number
        /^000.+$/,      // starting with more than 2 zeroes
        /^[0-1]+$/,     // bit pattern
        /^0\.\d+$/, // e.g. 0.12345678
        /^[0-1]-\d{5}-\d{3}-\d{1}$/,    // ISBN
        /^0-[0-1]\d{1}-\d{6}-\d{1}$/,   // ISBN
        /^0-[2-6]\d{2}-\d{5}-\d{1}$/,   // ISBN
        /^0-[7-8]\d{3}-\d{4}-\d{1}$/,   // ISBN
        /^0-8\d{4}-\d{3}-\d{1}$/,       // ISBN
        /^0-9\d{5}-\d{2}-\d{1}$/,       // ISBN
        /^0-9\d{6}-\d{1}-\d{1}$/,       // ISBN
        /^1\.\d{3}\.\d{3}$/,    // number with decimal separator
],

// list of special local phone number patterns and their corresponding country code
// here be dragons: always add [^\d]* at end of pattern
inclLocalList: [
        [/^[1-9]\d{2}[/\.-]\d{3}[/\.-]\d{4}[^\d]*$/, "+1"],     // US
        [/^\([1-9]\d{2}\) \d{3}[/\.-]\d{4}[^\d]*$/, "+1"],      // US
        [/^0[1-9][ \.]\d{2}[ \.]\d{2}[ \.]\d{2}[ \.]\d{2}[^\d]*$/, "+33"],      // France
        [/^0[ \.]800[ \.]\d{2}[ \.]\d{2}[ \.]\d{2}[^\d]*$/, "+33"],     // France
],

token_trigger: "+(0123456789",
token_part: " -/()[].\r\n"
        + String.fromCharCode(0xa0) // sc_nbsp
        + String.fromCharCode(0x2013) + String.fromCharCode(0x2014) +   String.fromCharCode(0x2212), // token_dash
token_start: "+(0",
token_sep: " -/(.",
token_disallowed_post: ":-²³°$€£¥",
token_disallowed_prev: "-,.$€£¥",
        /^0-[7-8]\d{3}-\d{4}-\d{1}$/,   // ISBN
        /^0-8\d{4}-\d{3}-\d{1}$/,       // ISBN
        /^0-9\d{5}-\d{2}-\d{1}$/,       // ISBN
        /^0-9\d{6}-\d{1}-\d{1}$/,       // ISBN
        /^1\.\d{3}\.\d{3}$/,    // number with decimal separator
],

// list of special local phone number patterns and their corresponding country code
// here be dragons: always add [^\d]* at end of pattern
inclLocalList: [
        [/^[1-9]\d{2}[/\.-]\d{3}[/\.-]\d{4}[^\d]*$/, "+1"],     // US
        [/^\([1-9]\d{2}\) \d{3}[/\.-]\d{4}[^\d]*$/, "+1"],      // US
        [/^0[1-9][ \.]\d{2}[ \.]\d{2}[ \.]\d{2}[ \.]\d{2}[^\d]*$/, "+33"],      // France
        [/^0[ \.]800[ \.]\d{2}[ \.]\d{2}[ \.]\d{2}[^\d]*$/, "+33"],     // France
],

token_trigger: "+(0123456789",
token_part: " -/()[].\r\n"
        + String.fromCharCode(0xa0) // sc_nbsp
        + String.fromCharCode(0x2013) + String.fromCharCode(0x2014) +   String.fromCharCode(0x2212), // token_dash
token_start: "+(0",
token_sep: " -/(.",
token_disallowed_post: ":-²³°$€£¥",
token_disallowed_prev: "-,.$€£¥",
        }
},


saveDialHistory: function()
{
        for (var i=0; i<objTelifyPrefs.maxHistory; i++) {
                if (this.dialHistory[i] == null) this.dialHistory[i] = "";
                objTelifyPrefs.telPrefs.setCharPref("history"+i, this.dialHistory[i]);
        }
},


updateDialHistory: function(prefix)
{
        //logmsg("updateDialHistory("+prefix+")");
        var name = objTelifyUtil.getCountryListString(prefix);
        if (name == null || name.length == 0) return;
        var newList = new Array(objTelifyPrefs.maxHistory);
        newList[0] = prefix;
        for (var i=0, j=1; i<objTelifyPrefs.maxHistory && j<objTelifyPrefs.maxHistory; i++) {
                if (this.dialHistory[i] == null || this.dialHistory[i] == "" || this.dialHistory[i] == prefix) continue;
                newList[j++] = this.dialHistory[i];
        }
        this.dialHistory = newList;
        this.saveDialHistory();
},


setStatus: function()
{
        var statusicon = document.getElementById("idTelify_statusicon");
        if (statusicon == null) return; // we have no status icon, so skip it
        if (objTelifyPrefs.fActive) {
                statusicon.setAttribute("src", "chrome://telify/content/icon/icon_menu.png");
                var text = objTelifyPrefs.telStrings.getString("telify_active");
                if (content.document.tel_parsetime) {
                        text += "\n" + objTelifyPrefs.telStrings.getString("processing_time") + " " + content.document.tel_parsetime + " ms";
                }
                statusicon.setAttribute("tooltiptext", text);
        } else {
                statusicon.setAttribute("src", "chrome://telify/content/icon/icon_menu_inactive.png");
                var text = objTelifyPrefs.telStrings.getString("telify_inactive");
                statusicon.setAttribute("tooltiptext", text);
        }
},



toggleBlacklist: function()
{
        var host = objTelifyUtil.getHost(content.document);
        if (host == null) return;
        if (objTelifyPrefs.excludedHosts.indexOf(host) >= 0) {
                objTelifyUtil.arrayRemove(objTelifyPrefs.excludedHosts, host);
        } else {
                objTelifyPrefs.excludedHosts.push(host);
        }
        objTelifyPrefs.blacklist = objTelifyPrefs.excludedHosts.join(",");
        objTelifyPrefs.telPrefs.setCharPref(objTelifyPrefs.PREF_BLACKLIST, objTelifyPrefs.blacklist);
},


toggleActive: function()
{
        objTelifyPrefs.telPrefs.setBoolPref(objTelifyPrefs.PREF_ACTIVE, !objTelifyPrefs.fActive);
        this.setStatus();
},


getSelectionNumber: function()
{
        //var sel = content.window.getSelection().toString();
        var sel = document.commandDispatcher.focusedWindow.getSelection().toString();
        sel = this.convertVanityNr(sel);
        sel = objTelifyUtil.stripNumber(sel);
        return sel;
},


dialNumber: function(nr)
{
        var requ = new XMLHttpRequest();
        var url = objTelifyUtil.createDialURL(nr);

        if (objTelifyPrefs.hrefType == objTelifyPrefs.HREFTYPE_CUSTOM) {
                if (objTelifyPrefs.custom_opentype == 1) {
                        window.open(url, "_blank");
                        return;
                }
                if (objTelifyPrefs.custom_opentype == 2) {
                        var browser = top.document.getElementById("content");
                        var tab = browser.addTab(url);
                        return;
                }
}

        try {
                requ.open("GET", url, true);
                requ.send(null);
        } catch(e) {
                // throws exception because answer is empty (or protocol is unknown)
                if (e.name == "NS_ERROR_UNKNOWN_PROTOCOL") {
                        objTelifyUtil.showMessageBox("", objTelifyLocale.msgUnknownProtocol(), objTelifyUtil.MB_ICON_ERROR);
                        objTelifyPrefs.showConfigDialog();
                }
        }
},


modifyPopup: function(event)
{
        var label, image, key;

        //var selText = content.window.getSelection().toString();
        var selText = document.commandDispatcher.focusedWindow.getSelection().toString();
);

        if (document.popupNode && document.popupNode.getAttribute("class") == "telified") {
                var nr = document.popupNode.getAttribute("nr");
                var posscc = document.popupNode.getAttribute("posscc");
                var pattcc = document.popupNode.getAttribute("pattcc");
                var nr_parts = objTelifyUtil.splitPhoneNr(nr);
                objTelify.modifyDialPopup(nr_parts[0], posscc, pattcc, nr_parts[1], "context");
                objTelifyUtil.setIdAttr("collapsed", false, "idTelify_menu_context");
        } else if (objTelifyPrefs.fActive && selText.length > 0 && objTelifyUtil.countDigits(selText) > 1) {
                var nr = objTelify.getSelectionNumber();
                var nr_parts = objTelifyUtil.splitPhoneNr(nr);
                objTelify.modifyDialPopup(nr_parts[0], null, null, nr_parts[1], "context");
                objTelifyUtil.setIdAttr("collapsed", false, "idTelify_menu_context");
        } else {
                objTelifyUtil.setIdAttr("collapsed", true, "idTelify_menu_context");
        }

        if (objTelifyPrefs.fActive) {
                label = objTelifyPrefs.telStrings.getString("telify_deactivate");
                image = "chrome://telify/content/icon/power_off.png";
        } else {


