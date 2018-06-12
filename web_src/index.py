def _makeIndexHTML(body, html_file, page_name):
    """ Generating HTML file for the Root index page """
    with open(html_file, "w") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {{
  box-sizing: border-box;
}}

#myInput {{
  background-position: 10px 12px;
  background-repeat: no-repeat;
  width: 100%;
  font-size: 16px;
  padding: 12px 20px 12px 40px;
  border: 1px solid #ddd;
  margin-bottom: 12px;
}}

#folder {{
  list-style-type: none;
  padding: 0;
  margin: 0;
}}

#folder li a {{
  border: 1px solid #ddd;
  margin-top: -1px; /* Prevent double borders */
  background-color: #b6b6b6;
  padding: 8px;
  text-decoration: none;
  font-size: 17px;
  color: black;
  display: block
}}

#folder li a:hover:not(.header) {{
  background-color: #eee;
}}

#file {{
  list-style-type: none;
  padding: 0;
  margin: 0;
}}

#file li a {{
  border: 1px solid #ddd;
  margin-top: -1px; /* Prevent double borders */
  background-color: #f6f6f6;
  padding: 8px;
  text-decoration: none;
  font-size: 17px;
  color: black;
  display: block
}}

#file li a:hover:not(.header) {{
  background-color: #eee;
}}
</style>
</head>
<body>
{BODY}
</body>
</html>
        """.format(PNM=page_name, BODY=body))


def generateNavigator(path, index_name=None):
    """ Creating a index.php page for simulation directories """
    t_start = time.time()
    if SIM_PATH not in path:
        GWarning(
            "Cannot create a navigator page for a directory outside \"/share/sim\".")
        return
    addr = path.replace(SIM_PATH, SIM_ADDR)
    if not index_name:
        index_name = path.split("/")[-1].upper()
    folders = [f for f in os.listdir(path) if os.path.isdir(path + "/" + f)]
    folders.sort()
    files = [f for f in os.listdir(path) if not os.path.isdir(
        path + "/" + f) and f != "index.php" and f != "navigator.php"]
    files.sort()
    hl_folders = [gweb.getHyperLink(addr + "/" + f, f, new_line=False, hover=False)
                  for f in folders]
    hl_files = [gweb.getHyperLink(addr + "/" + f, f, new_line=False, hover=False)
                for f in files]

    body = gweb.getHeader("Navigation for " + index_name, level=1)
    body += gweb.getHeader(
        gweb.getHyperLink(addr + "/index.php", "back", style="self", new_line=False, hover=False), level=4)
    usr = getpass.getuser()
    tstamp = timestamp()
    body += gweb.getHeader(
        "Latest modification by {U} at {T}".format(U=usr, T=tstamp), level=4)
    body += gweb.getHeader("Go to")
    body += "<input type=\"text\" id=\"myInput\" onkeyup=\"myFunction()\" placeholder=\"Search for keywords...\" title=\"SE\">\n"
    body += gweb.getList(hl_folders, ordered=False, id="folder")
    body += gweb.getList(hl_files, ordered=False, id="file")
    body += """
<script>
function cmp(s, flist) {
    var i;
    var l = flist.length;
    for(i = 0; i < l; i++){
        if(s.indexOf(flist[i]) == -1){
            return false;
        }
    }
    return true;
}
function myFunction() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("folder");
    li = ul.getElementsByTagName("li");
    len_li = li.length;
    for (i = 0; i < len_li; i++) {
        a = li[i].getElementsByTagName("a")[0];
        if (cmp(a.innerHTML.toUpperCase(), filter.split(" "))) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
    ul = document.getElementById("file");
    li = ul.getElementsByTagName("li");
    len_li = li.length;
    for (i = 0; i < len_li; i++) {
        a = li[i].getElementsByTagName("a")[0];
        if (cmp(a.innerHTML.toUpperCase(), filter.split(" "))) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
</script>
    """
    if os.path.exists(path + "/navigator.php"):
        os.remove(path + "/navigator.php")
    _makeIndexHTML(body, path + "/navigator.php", "Navigator")
    os.chmod(path + "/navigator.php", 0o777)
    delta_t = time.time() - t_start
    msg = "Created navigator for {A}, Time Usage: {T} sec.".format(
        A=addr, T=str(delta_t))
    GMessage(msg, TermColor.CYAN)
