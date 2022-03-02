function test_connection(user){
    if (process.env.AUTH_USERNAME == user.username && process.env.AUTH_PASSWORD == user.password){
        return true
    }
    return false
}

module.exports = test_connection