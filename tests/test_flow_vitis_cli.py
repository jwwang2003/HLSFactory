from hlsfactory.flow_vitis import (
    build_vitis_hls_cmd,
    build_vivado_cmd,
    get_vitis_bin,
    get_vivado_bin,
    uses_unified_cli,
)


def test_uses_unified_cli_from_bin_name(monkeypatch) -> None:
    monkeypatch.delenv("HLSFACTORY_IS_VIVADO_UNIFIED", raising=False)
    assert uses_unified_cli("/tools/Xilinx/Vitis/2025.1/bin/vitis-run")
    assert not uses_unified_cli("/tools/Xilinx/Vitis_HLS/2024.2/bin/vitis_hls")
    assert not uses_unified_cli("/tools/Xilinx/Vivado/2024.2/bin/vivado")


def test_uses_unified_cli_env_override(monkeypatch) -> None:
    monkeypatch.setenv("HLSFACTORY_IS_VIVADO_UNIFIED", "true")
    assert uses_unified_cli("/custom/wrapper")

    monkeypatch.setenv("HLSFACTORY_IS_VIVADO_UNIFIED", "false")
    assert not uses_unified_cli("/tools/Xilinx/Vitis/2025.1/bin/vitis-run")


def test_build_vitis_hls_cmd_supports_legacy_and_unified(monkeypatch) -> None:
    monkeypatch.delenv("HLSFACTORY_IS_VIVADO_UNIFIED", raising=False)

    assert (
        build_vitis_hls_cmd("/tools/Xilinx/Vitis_HLS/2024.2/bin/vitis_hls", "run.tcl")
        == "/tools/Xilinx/Vitis_HLS/2024.2/bin/vitis_hls -f run.tcl"
    )
    assert (
        build_vitis_hls_cmd("/tools/Xilinx/Vitis/2025.1/bin/vitis-run", "run.tcl")
        == "/tools/Xilinx/Vitis/2025.1/bin/vitis-run --mode hls --tcl run.tcl"
    )


def test_build_vivado_cmd_supports_legacy_and_unified(monkeypatch) -> None:
    monkeypatch.delenv("HLSFACTORY_IS_VIVADO_UNIFIED", raising=False)

    assert (
        build_vivado_cmd("/tools/Xilinx/Vivado/2024.2/bin/vivado", "run.tcl")
        == "/tools/Xilinx/Vivado/2024.2/bin/vivado -mode batch -source run.tcl"
    )
    assert (
        build_vivado_cmd("/tools/Xilinx/Vitis/2025.1/bin/vitis-run", "run.tcl")
        == "/tools/Xilinx/Vitis/2025.1/bin/vitis-run --mode vivado --tcl run.tcl"
    )


def test_get_vitis_bin_falls_back_between_legacy_and_unified(monkeypatch) -> None:
    monkeypatch.delenv("HLSFACTORY_IS_VIVADO_UNIFIED", raising=False)

    def which(cmd: str) -> str | None:
        return {
            "vitis_hls": None,
            "vitis-run": "/tools/Xilinx/Vitis/2025.1/bin/vitis-run",
        }.get(cmd)

    monkeypatch.setattr("hlsfactory.flow_vitis.shutil.which", which)
    assert get_vitis_bin() == "/tools/Xilinx/Vitis/2025.1/bin/vitis-run"


def test_get_vivado_bin_falls_back_between_legacy_and_unified(monkeypatch) -> None:
    monkeypatch.delenv("HLSFACTORY_IS_VIVADO_UNIFIED", raising=False)

    def which(cmd: str) -> str | None:
        return {
            "vivado": None,
            "vitis-run": "/tools/Xilinx/Vitis/2025.1/bin/vitis-run",
        }.get(cmd)

    monkeypatch.setattr("hlsfactory.flow_vitis.shutil.which", which)
    assert get_vivado_bin() == "/tools/Xilinx/Vitis/2025.1/bin/vitis-run"
