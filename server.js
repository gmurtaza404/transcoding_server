const fs = require('fs')
const http = require('http')
const util = require("util")
const os  = require("os")
var networkInterfaces = os.networkInterfaces( );

var measurement_run = true;
var requests_handled = 0;
// TODO: Remove this hardcode as well
web_pages = ["www.google.com","www.ask.com","www.dawnnews.tv","www.facebook.com","www.geo.tv","www.live.com","www.netflix","www.urdupoint.com","www.zemtv.com"] // fix hardcode

// TODO: Remove this hardcode.
device_memory_dictionary = {"SM-N920P":4, "HTC One M9":3, "Nokia 6.1":3, "Galaxy Nexus": 1, "wv": 2}

const phone_detail_regex =  /\(([^)]+)\)/
// Promises
const readFile = util.promisify(fs.readFile);

let current_directory =  process.cwd()



const decide_which_page_to_serve = (mem)=>{
    if (mem == 0.25){
        // serve low end page
        return "low_index.html"
    }else if(mem == 0.5){
        // serve medium end page
        return "mid_index.html"
    }else if(mem == 1){
        // serve ~ normal page
        return "high_index.html"
    }else if(mem == 2){
        // serve base page
        return "index.html"
    }else{
        // for now serve base page
        return "index.html"
    }

}

const find_mem_conf = (user_agent)=>{
    user_agent = user_agent.join(" ")
    phone_name = phone_detail_regex.exec(user_agent)[1].split(";")
    phone_name = phone_name[phone_name.length -1].split("Build")[0].trim()
    console.log(phone_name)
    try {
        return device_memory_dictionary[phone_name]    
    } catch (error) {
        console.log("Phone Name not in Database...")
        return 4
    }
}

const main = async ()=>{
    console.log("Starting the server")
    const server = http.createServer(async (req,resp) => {
        requests_handled = requests_handled + 1
        let response_string = ""
        //console.log(req.url)
        if(!measurement_run){
            raw_headers = req.rawHeaders
            user_agent = raw_headers[raw_headers.indexOf("User-Agent")+1].split(" ")
            //console.log(user_agent)
            try{
                if (user_agent.indexOf("Mobile") != -1){
                    // Serving memory aware page
                    if(req.url.search(/index.html/) == -1){
                        // normal request
                        response_string = await readFile(req.url.substr(1))
                    }else{
                        // device aware response
                        memory_conf_dev = find_mem_conf(user_agent)
                        //console.log(memory_conf_dev, user_agent)
                        request = req.url.replace("index.html", decide_which_page_to_serve(memory_conf_dev))
                        response_string = await readFile(request.substr(1))
                    }  
                }else{
                    // serving normal page.
                    //console.log(req.url.substr(1))
                    try{
                        response_string = await readFile(req.url.substr(1))
                    }catch(err){
                        console.log(err)
                    }
                    
                }
            }catch(err){
                response_string = "file not found!"
            }
        }else{
            //console.log(req.url)
            try{
                response_string = await readFile(req.url.substr(1))
            }catch(err){
                response_string = "file not found!"
            }
        }
        console.log(requests_handled)
        resp.end(response_string)
    })
    server.listen(8080, ()=> console.log('Listening on address:', networkInterfaces["wlp3s0"][0]["address"], "and port 8080"))
}


main()