from inserver import Application

app = Application(path="0.0.0.0")


@app.get("^/data$")
def get_data(request, response):
    data = {
        "people": [
            {
                "name": "Richard",
                "lastName": "Hendricks"
            },
            {
                "name": "Guy",
                "lastName": "Richy",
            },
        ],
    }
    response.json(200, data)


@app.get("^/$")
def index(request, response):
    response.json(200, {"hello": "world"})


@app.post("^/$")
def post(request, response):
    response.json(201, "\"created\"")


app.start()
