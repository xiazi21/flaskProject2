for s in {1,4,5,8,12,16}

do

	for i in {1..12}

	do 

		./proj3 1 $s sample_input/input_$i

		diff output/result-1-$s-input_$i sample_output/result-1-$s-input_$i

	done

	done

for s in {1,4,5,8,12,16}

do

	for i in {1..12}

	do 

		./proj3 2 $s sample_input/input_$i

		diff output/result-2-$s-input_$i sample_output/result-2-$s-input_$i

	done

	done
