#一行になっているfen形式の棋譜を、一手ごとに改行するプログラム
ns = ""
path = "C:/Users/m1261/Desktop/pgnToFen-master/blackkihu"##
(1..1683).each do |i|##
  file = File.join(path, "onelinefen/onelineblack_#{i}.fen")##
  outputfile = File.join(path, "fen/black_#{i}.fen")##
  File.open(file, 'r') do |f|
    f.each_line do |s|
      s.split(",").each_with_index do |part, index|
        ns += part
        ns += "\n" unless index == s.split("").length - 1
      end
      File.open(outputfile, "a") do |file|
        ns = ns.gsub("'", "")
        file.puts ns
        file.flush
      end
      ns = ""
    end
  end
  puts 'd'
end
