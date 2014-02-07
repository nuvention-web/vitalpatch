require 'spec_helper'

describe User do
  it "allows creation of users" do
    expect{
      User.create(email: "hi@hi.com")
    }.to change{User.count}.from(0).to(1)
  end

  it "rejects bad emails" do
    expect{
      User.create(email: "hi")
    }.to_not change{User.count}
  end

  it "doesn't allow duplicate emails" do
    email = "hi@hi.com"
    User.create!(email: email)
    expect{
      User.create(email: email)
    }.to_not change{User.count}
  end
end
