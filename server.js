const fs = require('fs')
const http = require('http')
const util = require("util")


// Promises
const readFile = util.promisify(fs.readFile);

let current_directory =  process.cwd()

const parse_url = (url)=>{
    return url.split("/")
}















const main = async ()=>{
    console.log("Starting the server")
    const server = http.createServer(async (req,resp) => {
        let response_string = "abc"
        try {
            console.log(req.url)

            elements = parse_url(req.url)
            console.log(elements[1] == "www.google.com")

            if (elements[1] == "www.google.com"){ // get rid of this hard code
                console.log("changing directory")
                process.chdir("WebPages/www.google.com")
                //console.log(elements[2])
                response_string = await readFile(elements[2])
            }else{
                console.log("hello")
                response_string = await readFile(req.url.substr(1))
            }

        }catch(err){
            console.log(err)
            response_string = "file not found"
        }
        resp.end(response_string)
    })






    server.listen(12000, ()=> console.log('Listening'))
}


main()