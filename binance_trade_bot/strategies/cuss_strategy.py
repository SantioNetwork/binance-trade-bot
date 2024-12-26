from binance_trade_bot.auto_trader import AutoTrader

from binance_trade_bot.auto_trader import AutoTrader

class Strategy(AutoTrader):

    def scout(self):
        """
        Scout for potential jumps from the current coin to another coin.
        Look for arbitrage opportunities with positive profit margins.
        """
        current_coin = self.db.get_current_coin()
        current_coin_price = self.manager.get_ticker_price(current_coin + self.config.BRIDGE)

        if current_coin_price is None:
            self.logger.info(f"Cannot scout: price for {current_coin + self.config.BRIDGE} not found.")
            return

        # Get profit ratios for all pairs involving the current coin
        ratio_dict = self._get_ratios(current_coin, current_coin_price)

        # Filter for profitable pairs
        profitable_pairs = {pair: ratio for pair, ratio in ratio_dict.items() if ratio > 0}

        if profitable_pairs:
            # Jump to the best coin based on the highest ratio
            best_pair = max(profitable_pairs, key=profitable_pairs.get)
            self.logger.info(f"Profitable opportunity: Jumping from {current_coin} to {best_pair.to_coin}.")
            self._jump_to_best_coin(current_coin, current_coin_price)
        else:
            self.logger.info("No profitable opportunities found. Retrying later.")
