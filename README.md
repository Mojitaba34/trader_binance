# Trader_binance
Bot for auto Trader in binance


## ApiProgram
- [ ] SignUp            -> All field from User Model.
- [ ] SignIn            -> Username or Email and Password.
- [ ] Auth with email   -> generate key and send for user email.
- [ ] Forget Password   -> send key for userEmail for change passwd.
- [ ] Generate ApiToken -> Generate and Save Token in Token Model for User.

## Gateway Models
- [ ] User              -> id, username, fullname, email, password.
- [ ] Token             -> id, Userid, title, description,Token,is_active.
- [ ] EmailAuth         -> id, userid, key, is_forget_pswd, is_active.