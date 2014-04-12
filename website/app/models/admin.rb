class Admin < ActiveRecord::Base
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable and :omniauthable

  # No registration in production
  if Rails.env.production?
    devise :database_authenticatable, :recoverable,
           :rememberable, :trackable, :validatable
  else
    devise :database_authenticatable, :registerable,
           :recoverable, :rememberable, :trackable, :validatable
  end
end
