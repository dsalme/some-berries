import pytest
from poke_berries.berries import calculate_berry_stats


class TestBerries:

    def test_calculate_berry_stats(self):
        fake_growth_times = [2,3,4,5,6]
        result = calculate_berry_stats(fake_growth_times)
        assert result.get("min_growth_time") == 2
        assert result.get("median_growth_time") == 4
        assert result.get("max_growth_time") == 6
        assert result.get("variance_growth_time") == 2.5
        assert result.get("mean_growth_time") == 4
        assert result.get("frequency_growth_time") == {2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
