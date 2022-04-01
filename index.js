const express = require('express')
const morgan = require('morgan')

const PORT = process.env.PORT || 5000
const app = express()


app.use(morgan('dev'))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))



app.listen(PORT, () => console.log(`Server up at http://localhost:${PORT}`))


const swaggerUi = require('swagger-ui-express')
const swaggerFile = require('./swagger_output.json')
app.use('/doc', swaggerUi.serve, swaggerUi.setup(swaggerFile))


require('./endpoints')(app)