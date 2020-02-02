import sunau
import random

def sample_zero(input_file, packet_size, loss):
	in_file = sunau.open(input_file, 'r')
	out_file = sunau.open("simulated_zero_"+input_file, 'w')
	out_file.setparams(in_file.getparams())
	i, total_frames = 1, in_file.getnframes()

	while i <= total_frames:
		f = in_file.readframes(packet_size)
		if random.randint(0,101) >= loss:
			out_file.writeframes(f)
		else:
			out_file.writeframes(bytes("00"*packet_size, 'utf-8'))

		i += packet_size

def sample_prev_packet(input_file, packet_size, loss):
	in_file = sunau.open(input_file, 'r')
	out_file = sunau.open("simulated_prevpacket_"+input_file, 'w')

	out_file.setparams(in_file.getparams())
	i, total_frames, f = 1, in_file.getnframes(), None
	prev = None
	print('total_frames:', total_frames)
	print('packet_size:', packet_size)

	while i <= total_frames:

		if f:
			prev = f
		f = in_file.readframes(packet_size)
		if random.randint(0,101) >= loss or not prev:
			out_file.writeframes(f)
		else:
			out_file.writeframes(prev)

		i += packet_size

def sample_prev_samp(input_file, packet_size, loss):
	in_file = sunau.open(input_file, 'r')
	out_file = sunau.open("simulated_prevsamp_"+input_file, 'w')

	out_file.setparams(in_file.getparams())
	i, total_frames, f = 1, in_file.getnframes(), None

	while i <= total_frames:

		f = in_file.readframes(packet_size-3)
		prev_samp = in_file.readframes(3)

		if random.randint(0,101) >= loss:
			out_file.writeframes(f)
			out_file.writeframes(prev_samp)
		else:
			out_file.writeframes(prev_samp*(packet_size//3))

		i += packet_size
		
sample_prev_packet('poe.au', 2500, 30)
sample_prev_samp('poe.au', 2500, 30)
sample_zero('poe.au', 2500, 30)


