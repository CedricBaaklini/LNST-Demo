from lnst.Controller.RecipeResults import ResultLevel
from lnst.RecipeCommon.Perf.PerfTestMixins import BasePerfTestTweakMixin
from lnst.Recipes.ENRT.PerfTestMixins.Utils import get_flow_measurements_from_config

class SctpFirewallPerfTestMixin(BasePerfTestTweakMixin):
    def apply_perf_test_tweak(self, perf_config):
        super().apply_perf_test_tweak(perf_config)

        flow_measurements = get_flow_measurements_from_config(perf_config)
        flow = flow_measurements[0].flows[0]
        if flow.type == "sctp_stream":
            for nic in [flow.generator_nic, flow.receiver_nic]:
                nic.netns.run(
                    "iptables -I OUTPUT ! -o %s -p sctp -j DROP" % nic.name,
                    job_level=ResultLevel.NORMAL,
                )

            tweak_config = perf_config.perf_test_tweak_config
            tweak_config["iptables_sctp"] = True

    def remove_perf_test_tweak(self, perf_config):
        flow_measurements = get_flow_measurements_from_config(perf_config)
        flow = flow_measurements[0].flows[0]
        if flow.type == "sctp_stream":
            for nic in [flow.generator_nic, flow.receiver_nic]:
                nic.netns.run(
                    "iptables -D OUTPUT ! -o %s -p sctp -j DROP" % nic.name,
                    job_level=ResultLevel.NORMAL,
                )
            tweak_config = perf_config.perf_test_tweak_config
            del tweak_config["iptables_sctp"]

        super().remove_perf_test_tweak(perf_config)

    def generate_perf_test_tweak_description(self, perf_config):
        description = super().generate_perf_test_tweak_description(perf_config)
        tweak_config = perf_config.perf_test_tweak_config
        if "iptables_sctp" in tweak_config:
            description.append(
                "added iptables rules to drop SCTP packets on other than "
                "tested interface"
                )
        else:
            description.append(
                "skipped addition of iptables rules to drop SCTP packets on "
                "other than tested interface"
                )

        return description
