class UserMailer < ActionMailer::Base
  default from: "vitalpatchteam@gmail.com"

  def welcome_email(user)
    mail(to: user.email, subject: 'Thanks for signing up!')
  end

  def send_mailchimp(user)
  	require 'mandrill'

	m = Mandrill::API.new "i1dg1XjDtJu4QOnuQvbrOA"

	html = "<!DOCTYPE html>
			<html>
			  <head>
			    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type' />
			  </head>
			  <body>
			    <h2>Thanks for signing up!</h2>
			    <p>We'll keep you updated on VitalPatch's development.</p>
			    <br>
			    <br>
			    <a href=\"*|UNSUB:http://vitalpatch.herokuapp.com/unsub|*\">Click here to unsubscribe.</a>
			  </body>
			</html>"

	message = {  
		:subject => "Thanks for signing up!",  
		:from_name => "Vital Patch Team",  
		:text => "We'll keep you updated on VitalPatch's development.",  
		:to =>[  
			{  
			 :email => user.email    
			}  
		],  
		:html => html,  
		:from_email => "vitalpatchteam@gmail.com"  
	}  
	sending = m.messages.send message  
	puts sending

	

	# postform = {
	# 				key: "i1dg1XjDtJu4QOnuQvbrOA",
	# 				message: {
	# 					html: html,
	# 					subject: "Thanks for signing up!",
	# 					from_email: "vitalpatchteam@gmail.com",
	# 					from_name: "Vital Patch Team",
	# 					to: [
	# 						{
	# 							email: user.email,
	# 							type: "to"
	# 						}
	# 					]
	# 				}
	# 			}

	# res = Net::HTTP.post_form(URI.parse("https://mandrillapp.com/api/1.0/messages/send.json"), postform)
	end
	# 	important: false,
	# 	track_opens: null,
	# 	track_clicks: null,
	# 	auto_text: null,
	# 	auto_html: null,
	# 	inline_css: null,
	# 	url_strip_qs: null,
	# 	preserve_recipients: null,	
	# 	view_content_link: null,
	# 	tracking_domain: null,
	# 	signing_domain: null,
	# 	return_path_domain: null,
	# 	merge: true,
	# 	"global_merge_vars": [
	# 		{
	# 			"name": "merge1",
	# 			"content": "merge1 content"
	# 		}
	# 	],
	# 	"merge_vars": [
	# 		{
	# 			"rcpt": "recipient.email@example.com",
	# 			"vars": [
	# 				{
	# 					"name": "merge2",
	# 					"content": "merge2 content"
	# 				}
	# 			]
	# 		}
	# 	],
	# 	"tags": [
	# 		"password-resets"
	# 	],
	# 	"subaccount": "customer-123",
	# 	"google_analytics_domains": [
	# 		"example.com"
	# 	],
	# 	"google_analytics_campaign": "message.from_email@example.com",
	# 	"metadata": {
	# 		"website": "www.example.com"
	# 	},
	# 	"recipient_metadata": [
	# 		{
	# 			"rcpt": "recipient.email@example.com",
	# 			"values": {
	# 				"user_id": 123456
	# 			}
	# 		}
	# 	],
	# 	"attachments": [
	# 		{
	# 			"type": "text/plain",
	# 			"name": "myfile.txt",
	# 			"content": "ZXhhbXBsZSBmaWxl"
	# 		}
	# 	],
	# 	"images": [
	# 		{
	# 			"type": "image/png",
	# 			"name": "IMAGECID",
	# 			"content": "ZXhhbXBsZSBmaWxl"
	# 		}
	# 	]
	# },
	# "async": false,
	# "ip_pool": "Main Pool",
	# "send_at": "example send_at"
# }

end
