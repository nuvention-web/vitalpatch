class HomeController < ApplicationController
  def index
  end

  def create
    @user = User.new(user_params)
    if @user.save
      redirect_to root_path, notice: "Successfully added"
    else
      redirect_to root_path, error: "Could not add: ~s" % @user.errors.full_messages
    end
  end

  private
  def user_params
    params.permit(:email)
  end
end
