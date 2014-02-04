require "spec_helper"

describe UserMailer do
  it "sends email" do
    user = User.create(email: "hi@hi.com")
    email = UserMailer.welcome_email(user)
    email.deliver
    expect(
      ActionMailer::Base.deliveries.last
    ).to eq(email)
  end
end
