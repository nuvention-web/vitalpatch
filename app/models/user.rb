class User < ActiveRecord::Base
  validates :email, :email => true
end
