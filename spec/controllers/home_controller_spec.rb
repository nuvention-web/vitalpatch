require 'spec_helper'

describe HomeController do
  describe 'GET index' do
    it 'succeeds' do
      get :index
      expect(response).to render_template("index")
    end
  end

  describe 'POST create' do
    it 'creates a user with valid email address' do
      expect{
        post :create, { email: "example@example.com" }
      }.to change{User.count}.from(0).to(1)
    end

    it "doesn't create a user with invalid email" do
      expect{
        post :create, { email: "sdfsdf" }
      }.to_not change{User.count}
    end
  end
end
