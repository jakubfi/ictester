#ifndef __LED_STRIP_H__
#define __LED_STRIP_H__

typedef struct rgb_color
{
	uint8_t red, green, blue;
} rgb_color;

void __attribute__((noinline)) led_strip_write(rgb_color *colors, uint16_t count);

#endif
