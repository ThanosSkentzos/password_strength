"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import math
from rxconfig import config


class Password(rx.State):
    len: int = 0
    strength: int = 0
    text: str = ""
    max_strength = 100

    def update_password(self, form_data):
        """Update password"""
        self.text = form_data
        # print('new pw:',self.text)
        self.calculate_strength()

    def calculate_strength(self):
        score = len(self.text)
        nums = "0123456789"
        lower = "abcdefghigklmnopqrstuvwxyz"
        upper = lower.upper()
        symbols = " ~`!@#$%^&*()_+-=][}{i\\|;':\",.<>/?"

        m = 0
        M = 64 * len(nums) * len(lower) * len(upper) * len(symbols)

        num_mult, lower_mult, upper_mult, symbol_mult = 1, 1, 1, 1
        for c in self.text:
            if c in nums:
                num_mult = len(nums)
            if c in lower:
                lower_mult = len(lower)
            if c in upper:
                upper_mult = len(upper)
            if c in symbols:
                symbol_mult = len(symbols)
        base_difficulty = num_mult * lower_mult * upper_mult * symbol_mult

        score = (
            math.log10(max(len(self.text), 1) * base_difficulty) / math.log10(M) * 100
        )

        self.strength = min(score, 100)


def index():
    return rx.center(
        rx.vstack(
            rx.vstack(
                rx.progress(value=Password.strength),
                rx.input(
                    name="input",
                    default_value="",
                    placeholder="Test your password...",
                    required=True,
                    max_length=64,
                    on_change=Password.update_password,
                    width=256,
                ),
            ),
        ),
    )


app = rx.App()
app.add_page(index)
