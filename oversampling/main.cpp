#include <iostream>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <math.h>

float sinc(float n) {
    return sin(M_PI * n) / (M_PI * n);
}

float sinc_y_value_at_x(float *input, int inputLength, float x) {
	float sum = 0.0;
	for (int i = 0; i < inputLength; i++) {
		sum += input[i] * sinc(x - float(i));
	}
	return sum;
}

void oversample_lerp(float *input, float *output, int inputLength) {
	for (int i = 0; i < inputLength - 1; i++) {
		float left = input[i];
		float right = input[i+1];

		output[2*i + 0] = input[i];
		output[2*i + 1] = 0.5 * (left + right);
	}
}

void oversample_fox(float *input, float *output, int inputLength) {
	float last = 0.0;

	for (int i = 0; i < inputLength; i++) {
		output[2*i + 0] = (last * 0.75f) + (input[i] * 0.25f);
		output[2*i + 1] = (last * 0.25f) + (input[i] * 0.75f);

		last = input[i];
	}
}

void oversample_sinc(float *input, float *output, int inputLength) {
	for (int i = 0; i < inputLength; i++) {
		if (i % 1000 == 0)
			std::cout << i << '\n';
		output[2*i + 0] = sinc_y_value_at_x(input, inputLength, float(i) + 0.1f);
		output[2*i + 1] = sinc_y_value_at_x(input, inputLength, float(i) + 0.6f);
	}
}

int main() {
	// 44100hz samplerate
	// RAW (header-less)
	// 32-bit float, mono
	int fd = open("ir_8khz.raw", O_RDONLY);
	if (fd == -1) {
		return 1;
	}

	struct stat fi;
	if (fstat(fd, &fi) == -1) {
		return 2;
	}

	int input_size = fi.st_size;
	if (input_size == 0) {
		return 3;
	}

	float *data = (float*)mmap(nullptr, input_size, PROT_READ, MAP_SHARED, fd, 0);

	// linear interpolation "oversampling"
	float *output_lerp = (float*)malloc(2 * input_size); // 2x oversampled
	oversample_lerp(data, output_lerp, input_size / sizeof(float));
	FILE *lerp_fd = fopen("oversampled_lerp.raw", "wb");
	fwrite(output_lerp, 2 * input_size, 1, lerp_fd);
	fclose(lerp_fd);
	free(output_lerp);

	// fox oversampling
	float *output_fox = (float*)malloc(2 * input_size); // 2x oversampled
	oversample_fox(data, output_fox, input_size / sizeof(float));
	FILE *fox_fd = fopen("oversampled_fox.raw", "wb");
	fwrite(output_fox, 2 * input_size, 1, fox_fd);
	fclose(fox_fd);
	free(output_fox);

	// sinc oversampling
	float *output_sinc = (float*)malloc(2 * input_size); // 2x oversampled
	oversample_sinc(data, output_sinc, input_size / sizeof(float));
	FILE *sinc_fd = fopen("oversampled_sinc.raw", "wb");
	fwrite(output_sinc, 2 * input_size, 1, sinc_fd);
	fclose(sinc_fd);
	free(output_sinc);

	close(fd);
	munmap(data, input_size);
}
