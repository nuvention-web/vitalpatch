class HomeController < ApplicationController
  def index
  end

  def create
    @user = User.new(user_params)
    if @user.save
      # Email
      UserMailer.send_mailchimp(@user)
      flash[:notice] = "Successfully added"
      redirect_to root_path
    else
      flash[:error] = "Could not add: %s" % @user.errors.full_messages
      redirect_to root_path
    end
  end

  def unsub
    email = URI.unescape(params[:md_email])
    user = User.where(email: email)
    puts email
    if user && user.destroy_all
      @message = "Your email " + email + " was successfully unsubscribed."
    else
      @message = "Sorry, there was an error: %s" % user.errors.full_messages
    end
  end

  private
  def user_params
    params.permit(:email)
  end
end
