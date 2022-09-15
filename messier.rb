require 'csv'

class Messier

	attr_reader :num
	attr_reader :constl
	attr_reader :weight

	def initialize(opt)
		@num = opt[:num]
		@constl = opt[:constl]
		@weight = opt[:weight]
	end

end

def parse(file)

	$list = []

	CSV.foreach(file) do |row|
	
		weights = [5, 4, 3, 2, 1]
		w = row[2].to_i

		n = weights[w - 1]
		n.times { $list << Messier.new(num: row[0], constl: row[1], weight: row[2].to_i) }
	end
end

def start

	diff = 5

	score = 0
	total = 0

	prev = nil

	while true

		# show obj from prev command call
		if prev.nil?
			obj = $list.sample
			until obj.weight <= diff
				obj = $list.sample
			end
		else 
			obj = prev
			prev = nil
		end

		# get input
		print "M#{obj.num} (#{obj.weight}) > "
		ans = gets.chomp.downcase

		# commands 
		if (ans == "exit")
			exit
		elsif (ans == "score")

			puts "score: #{score}/#{total}"
			puts ""
			prev = obj
			next

		elsif (ans =~ /diff [1-5]/)

			diff = ans.split[1].to_i
			score = 0
			total = 0
			puts "set max difficulty to #{diff}"
			puts ""

		else

			# check if constl is right
			if (ans == obj.constl.downcase)
				puts "correct"
				puts ""
				score += 1
				total += 1
			else
				puts "wrong: #{obj.constl}"
				puts ""
				total += 1
			end

		end
	end
end


if __FILE__ == $0
	parse("messier.csv")
	start
end