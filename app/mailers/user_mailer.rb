class UserMailer < ActionMailer::Base
  default from: "vitalpatchteam@gmail.com"

  def welcome_email(user)
    mail(to: user.email, subject: 'Thanks for signing up!')
  end
end
