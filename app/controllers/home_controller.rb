class HomeController < ApplicationController
  def index
  end

  def create
    @user = User.new(user_params)
    if @user.save
      flash[:notice] = "Successfully added"
      redirect_to root_path 
    else
      flash[:error] = "Could not add: %s" % @user.errors.full_messages
      redirect_to root_path
    end
  end

  private
  def user_params
    params.permit(:email)
  end
end
