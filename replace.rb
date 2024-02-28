#fen形式の棋譜の、アンパッサンとキャスリングの判定結果が入っている部分の位置を入れ替えるプログラム。stockfishでの形式に合わせるためのプログラム
path = "C:/Users/m1261/Desktop/pgnToFen-master/blackkihu"
(1594..1683).each do |i|
  fileb = File.join(path, "fen/black_#{i}.fen")
  outputfile = File.join(path, "replacedfen/replacedblack_#{i}.fen")

  inside_range = false  # "[r"が見つかった後、")]"が見つかるまでの間かどうかのフラグ

  File.open(fileb, 'r') do |f|
    File.open(outputfile, 'w') do |output_file|
      f.each_line do |line|
        if line.include?("[r")
          inside_range = true
        end

        if inside_range
          elements = line.split()
          if elements.length >= 4
            if elements[3].include?("])]}")
              elements[3].gsub!(/\]\)\]\}/, '')
              elements[2] += "])]}"
            elsif elements[3].include?("])")
              elements[3].gsub!(/\]\)/, '')
              elements[2] += "])"
            end
          end

          swapped_line = "#{elements[0]} #{elements[1]} #{elements[3]} #{elements[2]}"
          output_file.puts swapped_line
        else
          output_file.puts line
        end
        if line.include?(")]")
          inside_range = false
        end
      end
    end
  end
  
  #デバッグメッセージ
  puts "Processed file #{i}"
end
